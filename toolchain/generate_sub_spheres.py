#!/usr/bin/env python3
"""
Generate tier-2 sub-sphere enumeration for all 144 spheres.
Produces both the Section 3 markdown and the sub_sphere_registry.yaml.
"""

# Domain knowledge: sub-spheres for each of the 144 spheres
# Based on academic taxonomy, industry standards, and operational relevance

SUB_SPHERES = {
    # H01 Natural Sciences
    "S001_Physics": [
        "Classical Mechanics", "Quantum Mechanics", "Thermodynamics",
        "Electromagnetism", "Optics", "Nuclear Physics",
        "Particle Physics", "Condensed Matter", "Astrophysics",
        "Fluid Dynamics", "Plasma Physics", "Relativity"
    ],
    "S002_Chemistry": [
        "Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry",
        "Analytical Chemistry", "Biochemistry", "Polymer Chemistry",
        "Electrochemistry", "Photochemistry", "Computational Chemistry",
        "Materials Chemistry", "Environmental Chemistry", "Nuclear Chemistry"
    ],
    "S003_Biology": [
        "Molecular Biology", "Cell Biology", "Evolutionary Biology",
        "Microbiology", "Developmental Biology", "Marine Biology",
        "Neurobiology", "Immunology", "Bioinformatics",
        "Structural Biology", "Systems Biology", "Synthetic Biology"
    ],
    "S004_Astronomy": [
        "Observational Astronomy", "Stellar Astrophysics", "Galactic Astronomy",
        "Cosmology", "Planetary Science", "Radio Astronomy",
        "Space Science", "Astrochemistry", "Gravitational Astronomy",
        "Exoplanet Research", "Solar Physics", "Astrobiology"
    ],
    "S005_Geology": [
        "Mineralogy", "Petrology", "Geomorphology",
        "Tectonics", "Volcanology", "Seismology",
        "Stratigraphy", "Geochemistry", "Hydrogeology",
        "Economic Geology", "Engineering Geology", "Planetary Geology"
    ],
    "S006_Ecology": [
        "Population Ecology", "Community Ecology", "Ecosystem Ecology",
        "Conservation Biology", "Landscape Ecology", "Marine Ecology",
        "Behavioral Ecology", "Restoration Ecology", "Urban Ecology",
        "Microbial Ecology", "Chemical Ecology", "Theoretical Ecology"
    ],
    "S007_Genetics": [
        "Molecular Genetics", "Population Genetics", "Genomics",
        "Epigenetics", "Gene Therapy", "Genetic Engineering",
        "Pharmacogenomics", "Quantitative Genetics", "Evolutionary Genetics",
        "Human Genetics", "Agricultural Genetics", "Computational Genomics"
    ],
    "S008_Meteorology": [
        "Synoptic Meteorology", "Dynamic Meteorology", "Climate Science",
        "Atmospheric Chemistry", "Tropical Meteorology", "Mesoscale Meteorology",
        "Radar Meteorology", "Satellite Meteorology", "Agricultural Meteorology",
        "Aviation Meteorology", "Marine Meteorology", "Climate Modeling"
    ],
    "S009_Oceanography": [
        "Physical Oceanography", "Chemical Oceanography", "Biological Oceanography",
        "Geological Oceanography", "Ocean Engineering", "Deep Sea Research",
        "Coastal Oceanography", "Ocean Acoustics", "Polar Oceanography",
        "Ocean-Atmosphere Interaction", "Marine Geophysics"
    ],
    "S010_Paleontology": [
        "Vertebrate Paleontology", "Invertebrate Paleontology", "Paleobotany",
        "Micropaleontology", "Paleoecology", "Biostratigraphy",
        "Taphonomy", "Paleoanthropology", "Paleoclimatology",
        "Molecular Paleontology", "Ichnology"
    ],
    "S011_Zoology": [
        "Entomology", "Ornithology", "Herpetology",
        "Mammalogy", "Ichthyology", "Primatology",
        "Ethology", "Animal Physiology", "Parasitology",
        "Invertebrate Zoology", "Wildlife Biology", "Comparative Anatomy"
    ],
    "S012_Botany": [
        "Plant Physiology", "Plant Taxonomy", "Plant Ecology",
        "Mycology", "Phycology", "Bryology",
        "Ethnobotany", "Plant Pathology", "Palynology",
        "Plant Genetics", "Dendrology", "Agricultural Botany"
    ],

    # H02 Formal Sciences
    "S013_Mathematics": [
        "Algebra", "Analysis", "Geometry",
        "Topology", "Number Theory", "Combinatorics",
        "Probability Theory", "Applied Mathematics", "Numerical Analysis",
        "Mathematical Logic", "Category Theory", "Differential Equations"
    ],
    "S014_Logic": [
        "Propositional Logic", "Predicate Logic", "Modal Logic",
        "Fuzzy Logic", "Temporal Logic", "Deontic Logic",
        "Paraconsistent Logic", "Intuitionistic Logic", "Computational Logic",
        "Philosophical Logic", "Mathematical Logic", "Non-classical Logic"
    ],
    "S015_Statistics": [
        "Bayesian Statistics", "Frequentist Statistics", "Multivariate Analysis",
        "Time Series Analysis", "Spatial Statistics", "Nonparametric Statistics",
        "Biostatistics", "Econometrics", "Survey Methodology",
        "Statistical Learning", "Experimental Design", "Causal Inference"
    ],
    "S016_Computer_Science": [
        "Programming Languages", "Operating Systems", "Computer Architecture",
        "Databases", "Computer Networks", "Artificial Intelligence",
        "Computer Graphics", "Human-Computer Interaction", "Distributed Systems",
        "Compiler Design", "Theory of Computation", "Computer Security",
        "Machine Learning", "Natural Language Processing", "Computer Vision",
        "Software Architecture", "Parallel Computing", "Quantum Computing"
    ],
    "S017_Information_Theory": [
        "Coding Theory", "Data Compression", "Channel Capacity",
        "Entropy", "Signal Processing", "Error Correction",
        "Network Information Theory", "Quantum Information", "Rate-Distortion Theory",
        "Source Coding", "Algorithmic Information Theory"
    ],
    "S018_Game_Theory": [
        "Cooperative Games", "Non-cooperative Games", "Evolutionary Game Theory",
        "Mechanism Design", "Auction Theory", "Bargaining Theory",
        "Combinatorial Game Theory", "Algorithmic Game Theory", "Behavioral Game Theory",
        "Stochastic Games", "Mean Field Games"
    ],
    "S019_Operations_Research": [
        "Linear Programming", "Integer Programming", "Queuing Theory",
        "Inventory Theory", "Scheduling", "Network Optimization",
        "Simulation", "Stochastic Processes", "Dynamic Programming",
        "Metaheuristics", "Multi-objective Optimization", "Constraint Programming"
    ],
    "S020_Systems_Theory": [
        "General Systems Theory", "Cybernetics", "Complex Systems",
        "System Dynamics", "Control Theory", "Chaos Theory",
        "Network Theory", "Emergence", "Self-Organization",
        "Autopoiesis", "Viable System Model", "Sociotechnical Systems"
    ],
    "S021_Decision_Theory": [
        "Rational Choice Theory", "Prospect Theory", "Multi-criteria Decision Analysis",
        "Decision Under Uncertainty", "Behavioral Decision Theory", "Group Decision Making",
        "Sequential Decision Making", "Utility Theory", "Risk Analysis",
        "Judgment and Heuristics", "Preference Elicitation"
    ],
    "S022_Cryptography": [
        "Symmetric Cryptography", "Asymmetric Cryptography", "Hash Functions",
        "Digital Signatures", "Zero-Knowledge Proofs", "Homomorphic Encryption",
        "Post-Quantum Cryptography", "Blockchain Protocols", "Secure Multi-party Computation",
        "Cryptanalysis", "Key Management", "Privacy-Preserving Computation"
    ],
    "S023_Algorithmics": [
        "Sorting and Searching", "Graph Algorithms", "String Algorithms",
        "Computational Geometry", "Approximation Algorithms", "Randomized Algorithms",
        "Online Algorithms", "Streaming Algorithms", "Parallel Algorithms",
        "Distributed Algorithms", "Quantum Algorithms", "Algorithm Engineering"
    ],
    "S024_Data_Science": [
        "Data Mining", "Data Visualization", "Feature Engineering",
        "Big Data Systems", "Data Warehousing", "ETL Pipelines",
        "Predictive Analytics", "Recommender Systems", "Text Analytics",
        "Geospatial Analytics", "Real-time Analytics", "Data Governance"
    ],

    # H03 Social Sciences
    "S025_Sociology": [
        "Social Stratification", "Urban Sociology", "Medical Sociology",
        "Sociology of Religion", "Political Sociology", "Economic Sociology",
        "Cultural Sociology", "Organizational Sociology", "Environmental Sociology",
        "Digital Sociology", "Sociology of Education", "Social Movements"
    ],
    "S026_Psychology": [
        "Clinical Psychology", "Cognitive Psychology", "Developmental Psychology",
        "Social Psychology", "Neuropsychology", "Industrial-Organizational Psychology",
        "Health Psychology", "Forensic Psychology", "Positive Psychology",
        "Evolutionary Psychology", "Educational Psychology", "Psychometrics"
    ],
    "S027_Anthropology": [
        "Cultural Anthropology", "Physical Anthropology", "Linguistic Anthropology",
        "Archaeological Anthropology", "Medical Anthropology", "Economic Anthropology",
        "Political Anthropology", "Visual Anthropology", "Digital Anthropology",
        "Urban Anthropology", "Forensic Anthropology"
    ],
    "S028_Economics": [
        "Microeconomics", "Macroeconomics", "Development Economics",
        "International Economics", "Labor Economics", "Environmental Economics",
        "Behavioral Economics", "Health Economics", "Public Economics",
        "Financial Economics", "Agricultural Economics", "Institutional Economics"
    ],
    "S029_Political_Science": [
        "Comparative Politics", "International Relations", "Political Theory",
        "Public Administration", "Political Economy", "Electoral Systems",
        "Legislative Studies", "Judicial Politics", "Security Studies",
        "Political Communication", "Environmental Politics", "Computational Politics"
    ],
    "S030_Geography": [
        "Physical Geography", "Human Geography", "Economic Geography",
        "Political Geography", "Cultural Geography", "Urban Geography",
        "Biogeography", "Cartography", "GIS",
        "Remote Sensing", "Climate Geography", "Transport Geography"
    ],
    "S031_Linguistics": [
        "Phonetics", "Phonology", "Morphology",
        "Syntax", "Semantics", "Pragmatics",
        "Sociolinguistics", "Psycholinguistics", "Computational Linguistics",
        "Historical Linguistics", "Applied Linguistics", "Neurolinguistics"
    ],
    "S032_Demography": [
        "Population Dynamics", "Fertility Studies", "Mortality Studies",
        "Migration Studies", "Population Aging", "Population Policy",
        "Demographic Methods", "Historical Demography", "Spatial Demography",
        "Biodemography", "Family Demography"
    ],
    "S033_Criminology": [
        "Criminal Justice", "Victimology", "Penology",
        "Juvenile Delinquency", "White-collar Crime", "Cybercrime",
        "Forensic Science", "Policing Studies", "Restorative Justice",
        "Organized Crime", "Terrorism Studies", "Drug Policy"
    ],
    "S034_Social_Work": [
        "Clinical Social Work", "Community Organization", "Child Welfare",
        "Mental Health Social Work", "Gerontological Social Work", "School Social Work",
        "Medical Social Work", "Substance Abuse", "Family Services",
        "Social Policy", "International Social Work"
    ],
    "S035_Gender_Studies": [
        "Feminist Theory", "Masculinity Studies", "Queer Theory",
        "Gender and Development", "Gender and Health", "Gender and Law",
        "Intersectionality", "Transgender Studies", "Gender and Technology",
        "Reproductive Rights", "Gender and Work"
    ],
    "S036_Urban_Studies": [
        "Urban Planning", "Urban Economics", "Urban Sociology",
        "Smart Cities", "Housing Studies", "Urban Governance",
        "Urban Ecology", "Gentrification", "Urban Transportation",
        "Informal Settlements", "Urban Design", "Metropolitan Studies"
    ],

    # H04 Humanities
    "S037_History": [
        "Ancient History", "Medieval History", "Modern History",
        "Economic History", "Social History", "Military History",
        "Cultural History", "Intellectual History", "Digital History",
        "Environmental History", "World History", "Historiography"
    ],
    "S038_Philosophy": [
        "Metaphysics", "Epistemology", "Ethics",
        "Logic", "Aesthetics", "Political Philosophy",
        "Philosophy of Mind", "Philosophy of Science", "Philosophy of Language",
        "Existentialism", "Phenomenology", "Philosophy of Technology"
    ],
    "S039_Literature": [
        "Literary Theory", "Comparative Literature", "Poetry",
        "Fiction", "Drama", "Non-fiction",
        "Postcolonial Literature", "Digital Literature", "Children's Literature",
        "Genre Studies", "Translation Studies", "World Literature"
    ],
    "S040_Religious_Studies": [
        "Theology", "Comparative Religion", "Biblical Studies",
        "Islamic Studies", "Buddhist Studies", "Hindu Studies",
        "Sociology of Religion", "Philosophy of Religion", "Religion and Science",
        "New Religious Movements", "Mysticism", "Religious Ethics"
    ],
    "S041_Ethics": [
        "Applied Ethics", "Bioethics", "Environmental Ethics",
        "Business Ethics", "Technology Ethics", "AI Ethics",
        "Medical Ethics", "Research Ethics", "Animal Ethics",
        "Political Ethics", "Professional Ethics", "Metaethics"
    ],
    "S042_Classics": [
        "Greek Literature", "Latin Literature", "Classical Philosophy",
        "Ancient History", "Classical Archaeology", "Papyrology",
        "Epigraphy", "Numismatics", "Classical Reception",
        "Ancient Religion", "Classical Art"
    ],
    "S043_Archaeology": [
        "Prehistoric Archaeology", "Historical Archaeology", "Underwater Archaeology",
        "Landscape Archaeology", "Bioarchaeology", "Archaeometry",
        "Ethnoarchaeology", "Digital Archaeology", "Industrial Archaeology",
        "Experimental Archaeology", "Cultural Resource Management"
    ],
    "S044_Art_History": [
        "Ancient Art", "Medieval Art", "Renaissance Art",
        "Modern Art", "Contemporary Art", "Asian Art",
        "African Art", "Architecture History", "Photography History",
        "Digital Art History", "Art Criticism", "Visual Culture"
    ],
    "S045_Cultural_Studies": [
        "Popular Culture", "Media Culture", "Postcolonial Studies",
        "Diaspora Studies", "Memory Studies", "Food Studies",
        "Material Culture", "Digital Culture", "Subcultures",
        "Globalization Studies", "Heritage Studies", "Fan Studies"
    ],
    "S046_Folklore": [
        "Oral Traditions", "Mythology", "Folk Music",
        "Folk Art", "Fairy Tales", "Legend Studies",
        "Ritual Studies", "Ethnomusicology", "Folk Medicine",
        "Proverb Studies", "Material Folklore"
    ],
    "S047_Philology": [
        "Textual Criticism", "Manuscript Studies", "Paleography",
        "Etymology", "Historical Linguistics", "Comparative Philology",
        "Classical Philology", "Romance Philology", "Germanic Philology",
        "Slavic Philology", "Corpus Linguistics"
    ],
    "S048_Museology": [
        "Museum Management", "Exhibition Design", "Collection Management",
        "Conservation", "Museum Education", "Digital Museology",
        "Curatorial Studies", "Museum Ethics", "Community Museums",
        "Heritage Management", "Visitor Studies"
    ],

    # H05 Arts
    "S049_Visual_Arts": [
        "Drawing", "Printmaking", "Digital Art",
        "Installation Art", "Performance Art", "Video Art",
        "Mixed Media", "Conceptual Art", "Street Art",
        "Textile Art", "Ceramics", "Glass Art"
    ],
    "S050_Performing_Arts": [
        "Acting", "Directing", "Choreography",
        "Stage Design", "Costume Design", "Lighting Design",
        "Puppetry", "Circus Arts", "Opera",
        "Musical Theater", "Improvisation", "Physical Theater"
    ],
    "S051_Music": [
        "Music Composition", "Music Theory", "Music Production",
        "Sound Design", "Music Performance", "Conducting",
        "Music Technology", "Ethnomusicology", "Music Education",
        "Music Therapy", "Music Business", "Audio Engineering",
        "Streaming Platforms", "Electronic Music"
    ],
    "S052_Dance": [
        "Ballet", "Contemporary Dance", "Jazz Dance",
        "Hip Hop Dance", "Folk Dance", "Ballroom Dance",
        "Dance Therapy", "Dance Education", "Choreographic Theory",
        "Dance Technology", "Dance History"
    ],
    "S053_Theater": [
        "Playwriting", "Dramaturgy", "Stage Management",
        "Theater History", "Theater Criticism", "Community Theater",
        "Experimental Theater", "Children's Theater", "Political Theater",
        "Theater Technology", "Voice and Speech"
    ],
    "S054_Film": [
        "Screenwriting", "Cinematography", "Film Editing",
        "Film Direction", "Documentary", "Animation",
        "Visual Effects", "Sound Design for Film", "Film Production",
        "Interactive Cinema", "Virtual Production", "Motion Capture",
        "Streaming Content", "Short Film", "Film Distribution",
        "Film Criticism", "Film Festival"
    ],
    "S055_Creative_Writing": [
        "Fiction Writing", "Poetry Writing", "Screenwriting",
        "Playwriting", "Creative Non-fiction", "Game Narrative",
        "Interactive Fiction", "Lyric Writing", "Comedy Writing",
        "Science Fiction Writing", "Fantasy Writing", "Memoir"
    ],
    "S056_Architecture": [
        "Architectural Design", "Sustainable Architecture", "Urban Architecture",
        "Interior Architecture", "Landscape Architecture", "Computational Design",
        "Historic Preservation", "Parametric Design", "Building Technology",
        "Architectural Theory", "Vernacular Architecture", "Digital Architecture"
    ],
    "S057_Design": [
        "Graphic Design", "Industrial Design", "UX Design",
        "UI Design", "Service Design", "Fashion Design",
        "Interaction Design", "Game Design", "Type Design",
        "Motion Design", "Design Research", "Sustainable Design",
        "Accessibility Design"
    ],
    "S058_Photography": [
        "Portrait Photography", "Landscape Photography", "Documentary Photography",
        "Fashion Photography", "Architectural Photography", "Wildlife Photography",
        "Street Photography", "Commercial Photography", "Digital Photography",
        "Film Photography", "Photo Editing", "Photojournalism"
    ],
    "S059_Sculpture": [
        "Stone Sculpture", "Metal Sculpture", "Wood Sculpture",
        "Kinetic Sculpture", "Environmental Sculpture", "Digital Sculpture",
        "Ceramic Sculpture", "Found Object Art", "Monumental Sculpture",
        "Relief Sculpture", "Body Casting"
    ],
    "S060_Painting": [
        "Oil Painting", "Watercolor", "Acrylic Painting",
        "Fresco", "Encaustic", "Digital Painting",
        "Abstract Painting", "Figurative Painting", "Landscape Painting",
        "Mural Painting", "Miniature Painting"
    ],

    # H06 Engineering & Technology
    "S061_Mechanical_Engineering": [
        "Thermodynamics", "Fluid Mechanics", "Solid Mechanics",
        "Manufacturing Processes", "Machine Design", "Mechatronics",
        "HVAC", "Automotive Engineering", "Tribology",
        "Acoustics Engineering", "Biomechanics", "Computational Mechanics"
    ],
    "S062_Electrical_Engineering": [
        "Power Systems", "Control Systems", "Signal Processing",
        "Microelectronics", "Photonics", "Embedded Systems",
        "VLSI Design", "Power Electronics", "Instrumentation",
        "Antenna Design", "Electric Machines", "Renewable Energy Systems"
    ],
    "S063_Civil_Engineering": [
        "Structural Engineering", "Geotechnical Engineering", "Transportation Engineering",
        "Water Resources", "Construction Engineering", "Earthquake Engineering",
        "Coastal Engineering", "Bridge Engineering", "Tunnel Engineering",
        "Surveying", "Foundation Engineering", "Urban Infrastructure"
    ],
    "S064_Chemical_Engineering": [
        "Process Engineering", "Reaction Engineering", "Separation Processes",
        "Biochemical Engineering", "Polymer Engineering", "Petroleum Engineering",
        "Pharmaceutical Engineering", "Food Engineering", "Nanotechnology",
        "Catalysis", "Process Control", "Green Chemistry"
    ],
    "S065_Aerospace_Engineering": [
        "Aerodynamics", "Propulsion", "Orbital Mechanics",
        "Aircraft Design", "Spacecraft Design", "Avionics",
        "Flight Dynamics", "Rocket Engineering", "Satellite Systems",
        "Space Habitation", "Hypersonics", "UAV Design"
    ],
    "S066_Biomedical_Engineering": [
        "Medical Devices", "Tissue Engineering", "Biomaterials",
        "Medical Imaging", "Neural Engineering", "Rehabilitation Engineering",
        "Drug Delivery Systems", "Biosensors", "Prosthetics",
        "Bioinstrumentation", "Clinical Engineering", "Genetic Engineering"
    ],
    "S067_Environmental_Engineering": [
        "Water Treatment", "Air Quality", "Waste Treatment",
        "Remediation", "Environmental Impact Assessment", "Sustainable Engineering",
        "Noise Control", "Climate Engineering", "Ecological Engineering",
        "Environmental Monitoring", "Green Building"
    ],
    "S068_Industrial_Engineering": [
        "Production Systems", "Quality Engineering", "Ergonomics",
        "Supply Chain Engineering", "Lean Manufacturing", "Six Sigma",
        "Systems Engineering", "Reliability Engineering", "Safety Engineering",
        "Facilities Planning", "Work Measurement", "Automation"
    ],
    "S069_Software_Engineering": [
        "Requirements Engineering", "Software Architecture", "Software Testing",
        "DevOps", "Agile Methods", "Software Maintenance",
        "Formal Methods", "Software Security", "Cloud Engineering",
        "Mobile Development", "Embedded Software", "Open Source",
        "API Design", "Microservices", "Site Reliability Engineering"
    ],
    "S070_Materials_Engineering": [
        "Metallurgy", "Ceramics Engineering", "Polymer Engineering",
        "Composite Materials", "Nanomaterials", "Semiconductor Materials",
        "Biomaterials", "Smart Materials", "Corrosion Engineering",
        "Surface Engineering", "Materials Characterization", "Additive Manufacturing Materials"
    ],
    "S071_Nuclear_Engineering": [
        "Reactor Design", "Nuclear Safety", "Radiation Protection",
        "Nuclear Fuel Cycle", "Fusion Engineering", "Nuclear Waste Management",
        "Small Modular Reactors", "Nuclear Medicine Applications", "Decommissioning",
        "Nuclear Instrumentation"
    ],
    "S072_Robotics": [
        "Robot Kinematics", "Robot Control", "Autonomous Navigation",
        "Computer Vision for Robotics", "Manipulation", "Swarm Robotics",
        "Human-Robot Interaction", "Soft Robotics", "Medical Robotics",
        "Industrial Robotics", "Entertainment Robotics", "Space Robotics"
    ],

    # H07 Information & Communication
    "S073_Media_Studies": [
        "Media Theory", "Media Effects", "Political Communication",
        "Media Economics", "Media Ethics", "Audience Studies",
        "Media History", "New Media Studies", "Media Literacy",
        "Critical Media Studies", "Media and Society", "Transmedia"
    ],
    "S074_Journalism": [
        "Investigative Journalism", "Data Journalism", "Broadcast Journalism",
        "Digital Journalism", "Photojournalism", "Science Journalism",
        "Sports Journalism", "War Correspondence", "Citizen Journalism",
        "Journalism Ethics", "Longform Journalism", "Podcast Journalism"
    ],
    "S075_Telecommunications": [
        "Wireless Communications", "Optical Communications", "Network Protocols",
        "5G/6G Systems", "Satellite Communications", "Signal Processing",
        "Spectrum Management", "IoT Communications", "Network Security",
        "Mobile Networks", "Quantum Communications", "Edge Computing"
    ],
    "S076_Information_Systems": [
        "Enterprise Systems", "Database Management", "Business Intelligence",
        "IT Governance", "Systems Analysis", "Cloud Computing",
        "Information Security", "Knowledge Management", "Health Informatics",
        "E-Government", "Digital Transformation", "IT Service Management"
    ],
    "S077_Library_Science": [
        "Information Organization", "Cataloging", "Digital Libraries",
        "Information Retrieval", "Archives Management", "Preservation",
        "Reference Services", "Collection Development", "Metadata",
        "Open Access", "Research Data Management"
    ],
    "S078_Publishing": [
        "Book Publishing", "Academic Publishing", "Digital Publishing",
        "Magazine Publishing", "Self-Publishing", "Editorial Design",
        "Rights Management", "Publishing Technology", "Open Access Publishing",
        "Audio Publishing", "Comics and Graphic Novels"
    ],
    "S079_Advertising": [
        "Digital Advertising", "Brand Strategy", "Creative Direction",
        "Media Planning", "Programmatic Advertising", "Social Media Marketing",
        "Content Marketing", "Influencer Marketing", "Search Marketing",
        "Out-of-Home Advertising", "Advertising Ethics", "Ad Technology"
    ],
    "S080_Public_Relations": [
        "Corporate Communications", "Crisis Management", "Media Relations",
        "Reputation Management", "Internal Communications", "Government Relations",
        "Community Relations", "Digital PR", "Event Management",
        "Stakeholder Engagement", "CSR Communications"
    ],
    "S081_Digital_Media": [
        "Social Media Platforms", "Content Creation", "Streaming Media",
        "Digital Video", "Podcasting", "Web Design",
        "Mobile Media", "Virtual Reality Media", "Augmented Reality Media",
        "User-Generated Content", "Digital Distribution", "Platform Economics"
    ],
    "S082_Broadcasting": [
        "Television Production", "Radio Production", "Live Broadcasting",
        "Streaming Broadcasting", "Broadcast Engineering", "Program Scheduling",
        "Broadcast Regulation", "Sports Broadcasting", "News Broadcasting",
        "Community Broadcasting", "International Broadcasting"
    ],
    "S083_Film_Studies": [
        "Film Theory", "Film History", "National Cinemas",
        "Genre Studies", "Auteur Theory", "Film and Society",
        "Documentary Studies", "Animation Studies", "Film Preservation",
        "Film and Technology", "Spectatorship", "Film Sound Studies"
    ],
    "S084_Communication_Theory": [
        "Interpersonal Communication", "Mass Communication", "Organizational Communication",
        "Intercultural Communication", "Health Communication", "Science Communication",
        "Rhetoric", "Semiotics", "Discourse Analysis",
        "Nonverbal Communication", "Network Communication", "Risk Communication"
    ],

    # H08 Education
    "S085_Pedagogy": [
        "Constructivism", "Behaviorism in Education", "Critical Pedagogy",
        "Inquiry-Based Learning", "Project-Based Learning", "Experiential Learning",
        "Differentiated Instruction", "Culturally Responsive Teaching", "Universal Design for Learning",
        "Montessori Method", "Waldorf Education", "Flipped Classroom"
    ],
    "S086_Curriculum_Design": [
        "Curriculum Theory", "Standards-Based Design", "Backward Design",
        "Interdisciplinary Curriculum", "Competency-Based Education", "Curriculum Evaluation",
        "Hidden Curriculum", "Inclusive Curriculum", "STEM Curriculum",
        "Arts Integration", "Global Curriculum", "Curriculum Mapping"
    ],
    "S087_Educational_Psychology": [
        "Learning Theory", "Motivation", "Cognitive Development",
        "Social-Emotional Learning", "Metacognition", "Self-Regulated Learning",
        "Gifted Education", "Learning Disabilities", "Classroom Management",
        "Assessment Psychology", "Educational Neuroscience", "Growth Mindset"
    ],
    "S088_Special_Education": [
        "Inclusive Education", "Autism Spectrum", "Learning Disabilities",
        "Intellectual Disabilities", "Sensory Impairments", "Physical Disabilities",
        "Behavioral Disorders", "Assistive Technology", "Transition Planning",
        "Early Intervention", "Accessibility Standards", "Universal Design"
    ],
    "S089_Adult_Education": [
        "Andragogy", "Lifelong Learning", "Workplace Learning",
        "Continuing Education", "Community Education", "Literacy Programs",
        "Professional Development", "Vocational Training", "Distance Learning"
    ],
    "S090_E_Learning": [
        "Learning Management Systems", "Instructional Design", "Online Course Design",
        "Gamification", "Adaptive Learning", "Mobile Learning",
        "Microlearning", "Virtual Classrooms", "Learning Analytics",
        "Open Educational Resources", "MOOC Design", "Social Learning"
    ],
    "S091_Educational_Technology": [
        "EdTech Platforms", "AI in Education", "VR/AR in Education",
        "Classroom Technology", "Student Information Systems", "Digital Assessment",
        "Coding Education", "Robotics Education", "Maker Spaces",
        "Digital Literacy Education", "Technology Integration", "EdTech Policy"
    ],
    "S092_Assessment": [
        "Formative Assessment", "Summative Assessment", "Standardized Testing",
        "Performance Assessment", "Portfolio Assessment", "Rubric Design",
        "Item Response Theory", "Computer-Adaptive Testing", "Authentic Assessment",
        "Peer Assessment", "Self-Assessment", "Assessment Validity"
    ],
    "S093_Comparative_Education": [
        "Education Systems", "International Benchmarking", "Education Policy Transfer",
        "Cross-Cultural Studies", "Development Education", "Colonial Education Legacy",
        "Education Inequality", "Global Education Governance", "Regional Studies",
        "Education and Globalization"
    ],
    "S094_Education_Policy": [
        "School Governance", "Education Finance", "Teacher Policy",
        "Accountability Systems", "School Choice", "Education Reform",
        "Equity Policy", "Early Childhood Policy", "Higher Education Policy",
        "Education Law", "International Education Policy"
    ],
    "S095_Literacy": [
        "Reading Acquisition", "Functional Literacy", "Digital Literacy",
        "Numeracy", "Media Literacy", "Critical Reading",
        "Phonological Awareness", "Reading Comprehension", "Writing Development",
        "Multilingual Literacy", "Information Literacy"
    ],
    "S096_Higher_Education": [
        "University Governance", "Academic Freedom", "Research Universities",
        "Student Affairs", "Faculty Development", "Accreditation",
        "Graduate Education", "Community Colleges", "Internationalization",
        "University Rankings", "Academic Publishing", "Student Success"
    ],

    # H09 Health & Medicine
    "S097_Anatomy": [
        "Gross Anatomy", "Neuroanatomy", "Histology",
        "Embryology", "Comparative Anatomy", "Clinical Anatomy",
        "Radiological Anatomy", "Surgical Anatomy", "Functional Anatomy",
        "Developmental Anatomy", "Digital Anatomy"
    ],
    "S098_Pharmacology": [
        "Clinical Pharmacology", "Pharmacokinetics", "Pharmacodynamics",
        "Toxicology", "Psychopharmacology", "Pharmacogenomics",
        "Drug Discovery", "Pharmaceutical Chemistry", "Pharmacovigilance",
        "Regulatory Science", "Biopharmaceutics", "Natural Products"
    ],
    "S099_Psychiatry": [
        "Clinical Psychiatry", "Child Psychiatry", "Geriatric Psychiatry",
        "Addiction Psychiatry", "Forensic Psychiatry", "Consultation-Liaison",
        "Neuropsychiatry", "Community Psychiatry", "Psychotherapy",
        "Biological Psychiatry", "Social Psychiatry", "Telepsychiatry"
    ],
    "S100_Surgery": [
        "General Surgery", "Cardiac Surgery", "Neurosurgery",
        "Orthopedic Surgery", "Plastic Surgery", "Transplant Surgery",
        "Minimally Invasive Surgery", "Robotic Surgery", "Trauma Surgery",
        "Pediatric Surgery", "Vascular Surgery", "Surgical Oncology"
    ],
    "S101_Epidemiology": [
        "Infectious Disease Epidemiology", "Chronic Disease Epidemiology", "Molecular Epidemiology",
        "Environmental Epidemiology", "Social Epidemiology", "Genetic Epidemiology",
        "Pharmacoepidemiology", "Cancer Epidemiology", "Nutritional Epidemiology",
        "Outbreak Investigation", "Surveillance Systems", "Global Health Epidemiology"
    ],
    "S102_Public_Health": [
        "Health Promotion", "Disease Prevention", "Health Policy",
        "Global Health", "Occupational Health", "Environmental Health",
        "Maternal and Child Health", "Health Equity", "Health Systems",
        "Pandemic Preparedness", "Community Health", "Health Communication"
    ],
    "S103_Nursing": [
        "Clinical Nursing", "Nursing Education", "Nursing Research",
        "Community Health Nursing", "Pediatric Nursing", "Geriatric Nursing",
        "Mental Health Nursing", "Critical Care Nursing", "Nurse Practitioner",
        "Nursing Informatics", "Nursing Leadership", "Palliative Nursing"
    ],
    "S104_Dentistry": [
        "Orthodontics", "Periodontics", "Endodontics",
        "Oral Surgery", "Prosthodontics", "Pediatric Dentistry",
        "Dental Public Health", "Oral Pathology", "Dental Materials",
        "Implantology", "Digital Dentistry"
    ],
    "S105_Veterinary_Medicine": [
        "Small Animal Medicine", "Large Animal Medicine", "Veterinary Surgery",
        "Veterinary Pathology", "Veterinary Pharmacology", "Wildlife Medicine",
        "Aquatic Medicine", "Veterinary Public Health", "One Health",
        "Veterinary Genetics", "Exotic Animal Medicine"
    ],
    "S106_Nutrition": [
        "Clinical Nutrition", "Sports Nutrition", "Public Health Nutrition",
        "Nutritional Biochemistry", "Food Science", "Dietetics",
        "Nutrigenomics", "Pediatric Nutrition", "Geriatric Nutrition",
        "Community Nutrition", "Nutritional Epidemiology", "Functional Foods"
    ],
    "S107_Rehabilitation": [
        "Physical Therapy", "Occupational Therapy", "Speech Therapy",
        "Cardiac Rehabilitation", "Neurological Rehabilitation", "Pulmonary Rehabilitation",
        "Sports Rehabilitation", "Pediatric Rehabilitation", "Geriatric Rehabilitation",
        "Vocational Rehabilitation", "Assistive Technology", "Telerehabilitation"
    ],
    "S108_Pathology": [
        "Anatomical Pathology", "Clinical Pathology", "Molecular Pathology",
        "Cytopathology", "Hematopathology", "Neuropathology",
        "Forensic Pathology", "Dermatopathology", "Immunopathology",
        "Digital Pathology", "Surgical Pathology"
    ],

    # H10 Business & Economics
    "S109_Management": [
        "Strategic Management", "Operations Management", "Project Management",
        "Change Management", "Knowledge Management", "Innovation Management",
        "Risk Management", "Quality Management", "Leadership",
        "Organizational Behavior", "Decision Making", "Crisis Management"
    ],
    "S110_Marketing": [
        "Digital Marketing", "Brand Management", "Consumer Behavior",
        "Market Research", "Product Management", "Pricing Strategy",
        "Distribution Strategy", "B2B Marketing", "Services Marketing",
        "International Marketing", "Neuromarketing", "Marketing Analytics"
    ],
    "S111_Finance": [
        "Corporate Finance", "Investment Management", "Banking",
        "Financial Markets", "Derivatives", "Risk Management",
        "Fintech", "Behavioral Finance", "International Finance",
        "Personal Finance", "Insurance", "Quantitative Finance"
    ],
    "S112_Accounting": [
        "Financial Accounting", "Management Accounting", "Auditing",
        "Tax Accounting", "Forensic Accounting", "Government Accounting",
        "International Accounting", "Sustainability Reporting", "Accounting Information Systems",
        "Cost Accounting", "Accounting Ethics"
    ],
    "S113_Entrepreneurship": [
        "Startup Strategy", "Venture Capital", "Social Entrepreneurship",
        "Corporate Entrepreneurship", "Technology Entrepreneurship", "Family Business",
        "Franchising", "Business Model Innovation", "Lean Startup",
        "Entrepreneurial Finance", "Scaling", "Exit Strategy"
    ],
    "S114_Human_Resources": [
        "Talent Acquisition", "Compensation and Benefits", "Training and Development",
        "Performance Management", "Employee Relations", "Organizational Development",
        "HR Analytics", "Diversity and Inclusion", "Workforce Planning",
        "Employment Law", "HR Technology", "Remote Work Management"
    ],
    "S115_Operations_Management": [
        "Process Optimization", "Capacity Planning", "Inventory Management",
        "Total Quality Management", "Lean Operations", "Service Operations",
        "Facility Management", "Production Planning", "Maintenance Management",
        "Global Operations", "Sustainability Operations", "Digital Operations"
    ],
    "S116_Supply_Chain": [
        "Procurement", "Logistics", "Demand Planning",
        "Supply Chain Analytics", "Sustainable Supply Chain", "Global Supply Chain",
        "Supply Chain Risk", "Warehouse Management", "Last-Mile Delivery",
        "Supply Chain Technology", "Circular Supply Chain", "Cold Chain"
    ],
    "S117_International_Business": [
        "Cross-Cultural Management", "International Trade", "Foreign Direct Investment",
        "Global Strategy", "Emerging Markets", "International Negotiations",
        "Export Management", "International Joint Ventures", "Political Risk",
        "Global Talent Management", "International Finance", "Trade Policy"
    ],
    "S118_Business_Ethics": [
        "Corporate Social Responsibility", "Stakeholder Theory", "Ethical Leadership",
        "Corporate Governance", "Sustainability", "Whistleblowing",
        "Fair Trade", "Anti-Corruption", "Data Ethics",
        "Environmental Responsibility", "Labor Rights", "Ethical Supply Chain"
    ],
    "S119_Real_Estate": [
        "Commercial Real Estate", "Residential Real Estate", "Real Estate Finance",
        "Property Management", "Real Estate Development", "Real Estate Law",
        "Real Estate Valuation", "Urban Real Estate", "PropTech",
        "Real Estate Investment", "Sustainable Buildings"
    ],
    "S120_Macroeconomics": [
        "Monetary Policy", "Fiscal Policy", "Economic Growth",
        "Business Cycles", "International Macroeconomics", "Labor Markets",
        "Inflation", "Public Debt", "Central Banking",
        "Economic Forecasting", "Development Macroeconomics", "Digital Economy"
    ],

    # H11 Infrastructure
    "S121_Transportation": [
        "Road Transport", "Rail Transport", "Air Transport",
        "Maritime Transport", "Public Transit", "Autonomous Vehicles",
        "Electric Vehicles", "Traffic Engineering", "Transportation Planning",
        "Freight Transport", "Space Transport", "Hyperloop"
    ],
    "S122_Energy_Systems": [
        "Solar Energy", "Wind Energy", "Nuclear Power",
        "Hydroelectric Power", "Natural Gas", "Energy Storage",
        "Smart Grid", "Energy Efficiency", "Geothermal Energy",
        "Hydrogen Energy", "Energy Policy", "Carbon Capture"
    ],
    "S123_Water_Systems": [
        "Water Supply", "Wastewater Treatment", "Stormwater Management",
        "Water Distribution", "Desalination", "Water Quality",
        "Irrigation Systems", "Flood Control", "Water Conservation",
        "Groundwater Management", "Water Policy"
    ],
    "S124_Waste_Management": [
        "Solid Waste", "Hazardous Waste", "Recycling",
        "Composting", "Waste-to-Energy", "E-Waste",
        "Medical Waste", "Nuclear Waste", "Landfill Management",
        "Circular Economy", "Waste Reduction"
    ],
    "S125_Computing_Infrastructure": [
        "Data Centers", "Cloud Infrastructure", "Edge Computing",
        "Network Infrastructure", "Server Architecture", "Storage Systems",
        "Virtualization", "Container Orchestration", "CDN",
        "High-Performance Computing", "Quantum Computing Infrastructure", "Green Computing"
    ],
    "S126_Telecommunications_Infrastructure": [
        "Fiber Optics", "Cell Towers", "Submarine Cables",
        "Satellite Networks", "5G Infrastructure", "Network Operations",
        "Internet Exchange Points", "Last-Mile Infrastructure", "Spectrum Allocation",
        "Rural Connectivity", "Network Resilience"
    ],
    "S127_Urban_Planning": [
        "Land Use Planning", "Zoning", "Transportation Planning",
        "Environmental Planning", "Community Development", "Smart City Planning",
        "Housing Policy", "Public Space Design", "Regional Planning",
        "Participatory Planning", "Climate Adaptation Planning", "Heritage Conservation"
    ],
    "S128_Construction": [
        "Building Construction", "Heavy Construction", "Modular Construction",
        "Construction Management", "Building Materials", "Structural Systems",
        "Construction Safety", "Green Building", "BIM",
        "Prefabrication", "Demolition", "Construction Technology"
    ],
    "S129_Logistics": [
        "Supply Chain Logistics", "Warehouse Operations", "Fleet Management",
        "Route Optimization", "Reverse Logistics", "Cold Chain Logistics",
        "E-commerce Logistics", "Humanitarian Logistics", "Port Operations",
        "Customs and Trade", "Logistics Technology", "Last-Mile Solutions"
    ],
    "S130_Agriculture": [
        "Crop Science", "Animal Husbandry", "Precision Agriculture",
        "Organic Farming", "Aquaculture", "Agroforestry",
        "Agricultural Economics", "Food Processing", "Irrigation",
        "Soil Science", "Agricultural Technology", "Vertical Farming"
    ],
    "S131_Mining": [
        "Surface Mining", "Underground Mining", "Mineral Processing",
        "Mine Safety", "Environmental Mining", "Exploration Geology",
        "Mining Engineering", "Rare Earth Mining", "Deep Sea Mining",
        "Artisanal Mining", "Mine Closure"
    ],
    "S132_Manufacturing": [
        "Discrete Manufacturing", "Process Manufacturing", "Additive Manufacturing",
        "CNC Machining", "Assembly Systems", "Quality Control",
        "Smart Manufacturing", "Lean Manufacturing", "Semiconductor Manufacturing",
        "Pharmaceutical Manufacturing", "Food Manufacturing", "Sustainable Manufacturing"
    ],

    # H12 Law/Governance/Meta-Knowledge
    "S133_Constitutional_Law": [
        "Separation of Powers", "Fundamental Rights", "Judicial Review",
        "Federalism", "Constitutional Interpretation", "Amendment Process",
        "Comparative Constitutionalism", "Emergency Powers", "Electoral Law",
        "Constitutional History", "Digital Constitutionalism"
    ],
    "S134_Criminal_Law": [
        "Criminal Procedure", "Sentencing", "White-Collar Crime",
        "Cybercrime Law", "International Criminal Law", "Juvenile Justice",
        "Drug Law", "Terrorism Law", "Evidence Law",
        "Victim Rights", "Criminal Defense", "Prosecution"
    ],
    "S135_International_Law": [
        "Treaty Law", "International Humanitarian Law", "Law of the Sea",
        "International Trade Law", "International Environmental Law", "Diplomatic Law",
        "International Criminal Law", "Space Law", "Cyber Law",
        "International Organizations", "Sovereignty", "State Responsibility"
    ],
    "S136_Human_Rights": [
        "Civil Rights", "Political Rights", "Economic Rights",
        "Social Rights", "Cultural Rights", "Indigenous Rights",
        "Women's Rights", "Children's Rights", "Refugee Rights",
        "Disability Rights", "Digital Rights", "Environmental Rights"
    ],
    "S137_Corporate_Law": [
        "Company Formation", "Corporate Governance", "Mergers and Acquisitions",
        "Securities Regulation", "Bankruptcy", "Competition Law",
        "Contract Law", "Commercial Law", "Banking Law",
        "Insurance Law", "Corporate Compliance", "Shareholder Rights"
    ],
    "S138_Environmental_Law": [
        "Climate Change Law", "Pollution Control", "Biodiversity Law",
        "Water Law", "Land Use Law", "Environmental Impact Assessment",
        "Waste Law", "Energy Law", "Marine Environmental Law",
        "Environmental Justice", "Carbon Markets", "Green Finance Law"
    ],
    "S139_Intellectual_Property": [
        "Patent Law", "Copyright Law", "Trademark Law",
        "Trade Secrets", "IP Licensing", "Digital IP",
        "Pharmaceutical Patents", "Open Source Licensing", "IP Enforcement",
        "International IP", "AI and IP", "Indigenous Knowledge IP"
    ],
    "S140_Tax_Law": [
        "Income Tax", "Corporate Tax", "International Tax",
        "VAT/GST", "Tax Planning", "Tax Compliance",
        "Transfer Pricing", "Tax Policy", "Digital Taxation",
        "Estate Tax", "Tax Litigation"
    ],
    "S141_Public_Policy": [
        "Policy Analysis", "Policy Implementation", "Regulatory Policy",
        "Social Policy", "Economic Policy", "Health Policy",
        "Education Policy", "Technology Policy", "Environmental Policy",
        "Defense Policy", "Immigration Policy", "Urban Policy"
    ],
    "S142_Political_Theory": [
        "Liberalism", "Conservatism", "Socialism",
        "Anarchism", "Feminism", "Postcolonialism",
        "Communitarianism", "Republicanism", "Populism",
        "Green Political Theory", "Digital Democracy", "Global Justice"
    ],
    "S143_Diplomacy": [
        "Bilateral Diplomacy", "Multilateral Diplomacy", "Economic Diplomacy",
        "Cultural Diplomacy", "Public Diplomacy", "Digital Diplomacy",
        "Conflict Resolution", "Peace Negotiations", "Summit Diplomacy",
        "Track II Diplomacy", "Science Diplomacy"
    ],
    "S144_International_Relations": [
        "Realism", "Liberalism", "Constructivism",
        "Security Studies", "Foreign Policy Analysis", "International Organizations",
        "Global Governance", "Regional Integration", "Arms Control",
        "Cyber Security", "Climate Diplomacy", "Development Cooperation"
    ],
}


def generate_section3_markdown():
    """Generate Section 3 markdown content."""
    lines = []
    lines.append("## Section 3: Per-Sphere Sub-Sphere Enumeration\n")
    lines.append("### Methodology\n")
    lines.append("Sub-spheres derived from:\n")
    lines.append("- Academic taxonomy (standard university department structures)\n")
    lines.append("- Industry operational categories\n")
    lines.append("- Microsoft S4 subdomain audit (where applicable)\n")
    lines.append("- Federation routing requirements\n")
    lines.append("")
    lines.append("**Status key:** `populated` = named and ready for scoring | `BLANK` = slot empty, gap tracked\n\n")

    current_house = None
    total_populated = 0
    total_blanks = 0

    for sphere_key, subs in SUB_SPHERES.items():
        sphere_id = sphere_key.split("_")[0]
        sphere_name = sphere_key.split("_", 1)[1].replace("_", " ")
        house_num = int(sphere_id[1:]) // 12
        if int(sphere_id[1:]) % 12 == 0:
            house_num -= 1
        house_num = (int(sphere_id[1:]) - 1) // 12 + 1
        house_id = f"H{house_num:02d}"

        # House header
        house_names = {
            "H01": "Natural Sciences", "H02": "Formal Sciences",
            "H03": "Social Sciences", "H04": "Humanities",
            "H05": "Arts", "H06": "Engineering & Technology",
            "H07": "Information & Communication", "H08": "Education",
            "H09": "Health & Medicine", "H10": "Business & Economics",
            "H11": "Infrastructure", "H12": "Law/Governance/Meta-Knowledge"
        }
        if house_id != current_house:
            current_house = house_id
            lines.append(f"---\n\n### {house_id}: {house_names.get(house_id, '')}\n")

        # Sphere entry
        num_subs = len(subs)
        blank_count = max(0, 12 - num_subs) if num_subs < 12 else 0
        total_populated += num_subs
        total_blanks += blank_count

        lines.append(f"\n#### {sphere_id} {sphere_name} ({num_subs} populated, {blank_count} BLANK)\n")
        lines.append("| # | Sub-Sphere | Status |")
        lines.append("|---|-----------|--------|")
        for i, sub in enumerate(subs, 1):
            lines.append(f"| {sphere_id}.{i:02d} | {sub} | populated |")
        for i in range(num_subs + 1, 13):
            if num_subs < 12:
                lines.append(f"| {sphere_id}.{i:02d} | — | BLANK |")
        lines.append("")

    lines.append(f"\n---\n\n**Summary:** {total_populated} populated sub-spheres, {total_blanks} BLANKs across 144 spheres.\n")
    return "\n".join(lines)


def generate_registry_yaml():
    """Generate the sub_sphere_registry.yaml."""
    import yaml

    registry = {
        "version": "v3.5.0",
        "generated": "2026-04-29",
        "phase": "1.5",
        "total_spheres": 144,
        "total_sub_spheres_populated": 0,
        "total_blanks": 0,
        "wiggle_room_policy": {
            "minimum": 6,
            "standard": 12,
            "maximum": 24,
            "note": "No sphere should exceed 24 sub-spheres. Exceeding signals need for Phase 2 split."
        },
        "spheres": {}
    }

    total_pop = 0
    total_blank = 0

    for sphere_key, subs in SUB_SPHERES.items():
        sphere_id = sphere_key.split("_")[0]
        sphere_name = sphere_key.split("_", 1)[1].replace("_", " ")

        sub_sphere_list = []
        for i, sub in enumerate(subs, 1):
            sub_sphere_list.append({
                "id": f"{sphere_id}.{i:02d}",
                "name": sub,
                "status": "populated"
            })
            total_pop += 1

        blank_count = max(0, 12 - len(subs))
        for i in range(len(subs) + 1, 13):
            if len(subs) < 12:
                sub_sphere_list.append({
                    "id": f"{sphere_id}.{i:02d}",
                    "name": None,
                    "status": "BLANK"
                })
                total_blank += 1

        registry["spheres"][sphere_id] = {
            "name": sphere_name,
            "sub_spheres": sub_sphere_list,
            "populated_count": len(subs),
            "blank_count": blank_count,
            "population_priority": "high" if blank_count > 4 else ("medium" if blank_count > 0 else "complete")
        }

    registry["total_sub_spheres_populated"] = total_pop
    registry["total_blanks"] = total_blank

    return registry


if __name__ == "__main__":
    import yaml
    import os

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Generate Section 3 markdown
    section3 = generate_section3_markdown()
    section3_path = os.path.join(base, "houses", "h00_directory", "ontology_v3.5_section3.md")
    with open(section3_path, "w") as f:
        f.write(section3)
    print(f"Written: {section3_path}")

    # Generate registry YAML
    registry = generate_registry_yaml()
    registry_path = os.path.join(base, "houses", "h00_directory", "sub_sphere_registry.yaml")
    with open(registry_path, "w") as f:
        yaml.dump(registry, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    print(f"Written: {registry_path}")

    # Stats
    print(f"\nStats:")
    print(f"  Total spheres: 144")
    print(f"  Total populated sub-spheres: {registry['total_sub_spheres_populated']}")
    print(f"  Total BLANKs: {registry['total_blanks']}")
    print(f"  Average sub-spheres per sphere: {registry['total_sub_spheres_populated']/144:.1f}")

    # Vast domains (>12)
    vast = [(k, v["populated_count"]) for k, v in registry["spheres"].items() if v["populated_count"] > 12]
    if vast:
        print(f"\n  Vast domains (>12 sub-spheres):")
        for sid, count in sorted(vast, key=lambda x: -x[1]):
            print(f"    {sid}: {count}")
