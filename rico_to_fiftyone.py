import fiftyone as fo
import fiftyone.brain as fob
import json
import os
import numpy as np

def convert_bounds_to_relative(bounds, img_width=1440, img_height=2560):
    """
    Convert absolute pixel coordinates to relative coordinates required by FiftyOne
    
    Args:
        bounds (list): Absolute pixel coordinates in format [left, top, right, bottom]
        img_width (int): Width of image in pixels (default 1440)
        img_height (int): Height of image in pixels (default 2560)
        
    Returns:
        list: Relative coordinates in format [x, y, width, height] normalized to [0,1]
    """
    x = bounds[0] / img_width
    y = bounds[1] / img_height
    width = (bounds[2] - bounds[0]) / img_width 
    height = (bounds[3] - bounds[1]) / img_height
    return [x, y, width, height]

def process_ui_element(element):
    """
    Convert a UI element dictionary into a FiftyOne Detection object
    
    Args:
        element (dict): Dictionary containing UI element information including:
            - bounds: Bounding box coordinates [left, top, right, bottom]
            - componentLabel: Label identifying the UI component type
            - iconClass (optional): Class name for icon elements
            - text (optional): Text content of the element
            - textButtonClass (optional): Class name for text buttons
            - clickable (optional): Boolean indicating if element is clickable
            - class (optional): Element class type
            - resource-id (optional): Android resource ID
    
    Returns:
        fo.Detection or None: FiftyOne Detection object if valid element, None otherwise
    """
    # Create a copy and remove ancestors to avoid processing unnecessary hierarchy info
    element = element.copy()
    element.pop('ancestors', None)
    
    # Skip if required fields are missing
    if 'bounds' not in element or 'componentLabel' not in element:
        return None
        
    # Convert bbox coordinates to relative format
    rel_box = convert_bounds_to_relative(element['bounds'])
    
    # Get text content with priority order:
    # 1. iconClass (for icons)
    # 2. text (for text elements)
    # 3. textButtonClass (for text buttons)
    text_content = element.get('iconClass', 
                   element.get('text',
                   element.get('textButtonClass', None)))
    
    # Create and return Detection object with all relevant attributes
    return fo.Detection(
        label=element['componentLabel'],
        bounding_box=rel_box,
        content_or_function=text_content,
        clickable=element.get('clickable', False),
        type=element.get('class', ''),
        resource_id=element.get('resource-id', '')
    )

def process_recursively(element, detections):
    """
    Recursively process UI elements and their children at any depth
    
    Traverses the UI element tree and processes each element that contains
    valid detection information, including all nested children at any depth.
    
    Args:
        element (dict): UI element dictionary that may contain children
        detections (list): List to accumulate Detection objects
    """
    # Process current element if valid
    detection = process_ui_element(element)
    if detection:
        detections.append(detection)
    
    # Recursively process any children elements
    if 'children' in element:
        for child in element['children']:
            process_recursively(child, detections)

def create_rico_dataset():
    """
    Create a FiftyOne dataset from RICO UI screenshots and annotations
    
    The function:
    - Creates FiftyOne samples for each UI screenshot
    - Processes and adds UI element detections
    - Adds 64-dimensional UI layout vectors that encode layout based on 
      text and image distribution
    
    Returns:
        fo.Dataset: FiftyOne dataset containing the processed samples with:
            - filepath: Path to UI screenshot
            - detections: List of UI element detections
            - ui_vector: 64-dim layout vector encoding text/image distribution
    """
    dataset = fo.Dataset("rico_dataset")
    
    # Set up paths to data directories
    combined_dir = os.path.abspath("combined")  # Contains UI screenshots
    semantic_dir = os.path.abspath("semantic_annotations")  # Contains annotations and masks
    
    # Load UI vector data
    # ui_names.json maps filenames to indices in ui_vectors.npy
    with open('ui_layout_vectors/ui_names.json') as f:
        ui_names = json.load(f)
    # ui_vectors.npy contains 64-dim vectors encoding UI layouts
    ui_vectors = np.load('ui_layout_vectors/ui_vectors.npy')
    
    # Create mapping from filename to vector index for efficient lookup
    filename_to_index = {name: idx for idx, name in enumerate(ui_names['ui_names'])}
    
    samples = []
    
    # Process each screenshot in the combined directory
    for filename in os.listdir(combined_dir):
        if filename.endswith('.jpg'):
            sample_id = filename.replace('.jpg', '')
            
            # Create new sample with screenshot image
            sample = fo.Sample(filepath=os.path.join(combined_dir, filename))
            
            # Convert jpg filename to png for UI vector lookup
            png_filename = f"{sample_id}.png"
            
            # Add UI vector if available for this sample
            if png_filename in filename_to_index:
                vector_idx = filename_to_index[png_filename]
                ui_vector = ui_vectors[vector_idx, :]
                # Convert numpy array to list for MongoDB storage
                sample['ui_vector'] = ui_vector.tolist()
            
            # Get paths to corresponding annotation files
            json_path = os.path.join(semantic_dir, f"{sample_id}.json")
            mask_path = os.path.join(semantic_dir, f"{sample_id}.png")
            
            if os.path.exists(json_path):
                # Load and process semantic annotations
                with open(json_path) as f:
                    semantic_data = json.load(f)
                
                detections = []
                # Process all children recursively to get UI element detections
                for child in semantic_data.get('children', []):
                    process_recursively(child, detections)
                
                # Add detections to sample if any were found
                if detections:
                    sample['detections'] = fo.Detections(detections=detections)
            
            samples.append(sample)
    
    # Add all processed samples to dataset at once for efficiency
    dataset.add_samples(samples, dynamic=True)
    dataset.compute_metadata()
    
    return dataset


if __name__ == "__main__":
    # Create the FiftyOne dataset from RICO data
    rico_dataset = create_rico_dataset()
    
    rico_dataset.persistent = True
    
    fob.compute_visualization(
    dataset,
    embeddings="ui_vector",
    method="umap",
    create_index=True,
    brain_key="ui_viz",
    random_seed=51,
)
