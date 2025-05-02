# Parse the RICO dataset into FiftyOne Format


# Rico Semantic Dataset Details

## Dataset Description
**Curated by:** Thomas F. Liu, Mark Craft, Jason Situ, Ersin Yumer, Radomir Mech, and Ranjitha Kumar (University of Illinois at Urbana-Champaign and Adobe Systems Inc.)

**Funded by:** Adobe research donation, Google Faculty Research Award, and NSF Grant IIS-1750563

**Shared by:** The Interaction Mining Group at University of Illinois at Urbana-Champaign

**Language(s):** English (en)

**License:** Research use (specific license terms not explicitly stated in documentation)

## Dataset Sources
**Website:** http://interactionmining.org/rico

**Paper:** Liu, T. F., Craft, M., Situ, J., Yumer, E., Mech, R., & Kumar, R. (2018). [Learning Design Semantics for Mobile Apps](https://www.ranjithakumar.net/resources/mobile-semantics.pdf). In The 31st Annual ACM Symposium on User Interface Software and Technology (UIST '18).

**Repo:** https://github.com/datadrivendesign/semantic-icon-classifier (Semantic icon classifier implementation)

## Uses
### Direct Use
- Training interface design search engines to find similar UI designs
- Developing generative AI models for UI layout creation
- Training models that automatically generate code from UI designs
- Building tools that understand the meaning and function of UI elements
- Analyzing design patterns across different app categories
- Teaching design systems to recognize component types and their usage patterns
- Researching relationships between visual design and interface functionality

### Out-of-Scope Use
- Extracting personal or identifiable user information
- Generating deceptive interfaces that might mislead users
- Making judgments about individual users based on interaction patterns
- Commercial redistribution without appropriate permissions
- Creating applications that violate app store design guidelines or terms of service

## Dataset Structure
The semantic subset contains:
- 66,000+ annotated UI screens from mobile applications
- Semantic screenshots with UI elements color-coded by type (components, buttons, icons)
- Detailed hierarchies where each element includes semantic annotations

Each UI element in the hierarchy includes:
- Component classification (e.g., Icon, Text Button, List Item)
- Functional classification (e.g., "login" for text buttons, "cart" for icons)
- Original properties (bounds, class, resource-id, etc.)

## Dataset Creation
### Curation Rationale
The dataset was created to expose the semantic meaning of mobile UI elements - what they represent and how they function. While prior datasets captured visual design, this semantic layer enables deeper understanding of interface functionality across applications, supporting more advanced design tools and research.

### Source Data
#### Data Collection and Processing
1. Started with the Rico dataset of 9.3k Android apps spanning 27 categories
2. Created a lexical database through iterative open coding of 73,000+ UI elements and 720 screens
3. Developed code-based patterns to detect different component types
4. Trained a convolutional neural network (94% accuracy) to classify icons
5. Implemented anomaly detection to distinguish between icons and general images
6. Applied these techniques to generate semantic annotations for 78% of visible elements in the dataset

#### Who are the source data producers?
The original UI designs were created by Android app developers whose applications were available on the Google Play Store. The applications spanned 27 categories and had an average user rating of 4.1.

### Annotations
#### Annotation process
1. Referenced design libraries (e.g., Material Design) to establish initial vocabulary
2. Performed iterative open coding of 720 screens to identify 24 UI component categories
3. Extracted and clustered 20,386 unique button text strings to identify 197 text button concepts
4. Analyzed 73,449 potential icons to determine 97 icon classes
5. Used machine learning and heuristic approaches to scale annotation to the full dataset
6. Generated color-coded semantic screenshots to visualize element types

#### Who are the annotators?
The annotation framework was developed by researchers from University of Illinois at Urbana-Champaign and Adobe Systems Inc. The initial coding involved three researchers using a consensus-driven approach, with subsequent scaling through machine learning techniques.

### Personal and Sensitive Information
The dataset focuses on UI design elements rather than user data. Screenshots were captured during controlled exploration sessions rather than from real user data. While some screens might contain placeholder text mimicking personal information, the dataset does not appear to contain actual personal or sensitive information from real users.

## Bias, Risks, and Limitations
- Limited to Android mobile applications (no iOS or web interfaces)
- Represents design practices from around 2017-2018 (may not reflect current trends)
- Biased toward successful apps (average rating 4.1)
- Incomplete coverage (78% of visible elements receive semantic annotations)
- Icon classifier has lower accuracy for underrepresented classes
- May not adequately represent cultural or regional UI design variations
- Limited to apps with English-language interfaces

## Recommendations
Users should be aware that:
- The dataset represents a specific snapshot in time of mobile design practices
- Not all UI elements receive semantic annotations
- The dataset might exhibit biases toward certain design patterns popular in high-rated apps
- Applications built on this dataset should validate results against contemporary design standards

## Dataset Card Contact
The dataset is maintained by the Interaction Mining Group at the University of Illinois at Urbana-Champaign. Contact information can be found at: http://interactionmining.org/


# Citation

```bibtex
@inproceedings{deka2017rico,
  title     = {Rico: A mobile app dataset for building data-driven design applications},
  author    = {Deka, Biplab and Huang, Zifeng and Franzen, Chad and Hibschman, Joshua and Afergan, Daniel and Li, Yang and Nichols, Jeffrey and Kumar, Ranjitha},
  booktitle = {Proceedings of the 30th annual ACM symposium on user interface software and technology},
  pages     = {845--854},
  year      = {2017}
}
```

```bibtex
@inproceedings{liu2018learning,
  title={Learning Design Semantics for Mobile Apps},
  author={Liu, Thomas F and Craft, Mark and Situ, Jason and Yumer, Ersin and Mech, Radomir and Kumar, Ranjitha},
  booktitle={The 31st Annual ACM Symposium on User Interface Software and Technology},
  year={2018}
}
```