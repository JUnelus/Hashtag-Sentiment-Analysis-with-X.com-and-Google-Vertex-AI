from google.cloud import aiplatform

# Initialize Vertex AI
aiplatform.init(project="our-forest-429717-g5", location="us-central1")

# **Get the import schema URI**
import_schema_uri = aiplatform.schema.dataset.ioformat.image.multi_label_classification

# **Create the Dataset object**
dataset = aiplatform.ImageDataset.create(
    display_name='rotten-apples-dataset',
    gcs_source='gs://jimmy_image_bucket/rottenapples',
    import_schema_uri=import_schema_uri  # Add this line
)

job = aiplatform.AutoMLImageTrainingJob(
    display_name="fruit-classifier",
    prediction_type="classification",
    multi_label=False,
)

model = job.run(
    dataset=dataset,  # Now the dataset variable is defined
    model_display_name="fruit-classifier",
    budget_milli_node_hours=8000,
)