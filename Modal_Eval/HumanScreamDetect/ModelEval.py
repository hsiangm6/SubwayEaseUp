import torch
import torchaudio
from PIL import Image
from matplotlib import pyplot as plt
from torchvision.transforms import transforms

# Define a function to transform audio data into images
def transform_data_to_image(audio, sample_rate):
    spectrogram_tensor = (torchaudio.transforms.MelSpectrogram(sample_rate=sample_rate, n_mels=64, n_fft=1024)(audio)[0] + 1e-10).log2()
    # Save the spectrogram as an image
    image_path = f'voice_image.png'
    plt.imsave(image_path, spectrogram_tensor.numpy(), cmap='viridis')
    return image_path

def process_file(filename, model):
    # Select device
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    # Set the model to evaluation mode
    model.eval()

    # Convert to device
    model.to(device)

    # Define the image transformation pipeline
    transform = transforms.Compose([
        transforms.Resize((64, 862)),
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x[:3, :, :])
    ])

    # Load the audio
    audio, sample_rate = torchaudio.load(filename)

    # Transform audio to an image and save it
    image_path = transform_data_to_image(audio, sample_rate)

    # Load the saved image and apply transformations
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)  # Add batch dimension

    # Make predictions using the model
    model.eval()
    with torch.no_grad():
        outputs = model(image.to(device))

    print(outputs)

    predict = outputs.argmax(dim=1).cpu().detach().numpy().ravel()[0]

    return predict == 1
