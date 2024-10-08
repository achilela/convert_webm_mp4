import streamlit as st
import os
import tempfile
import cv2
import numpy as np

def preprocess_webm(input_file_path):
    # Create a temporary directory to store the preprocessed file
    with tempfile.TemporaryDirectory() as temp_dir:
        preprocessed_filename = os.path.splitext(os.path.basename(input_file_path))[0] + "_preprocessed.webm"
        preprocessed_path = os.path.join(temp_dir, preprocessed_filename)

        # Run ffmpeg to preprocess the file
        ffmpeg.input(input_file_path).output(preprocessed_path, codec='copy').run()

        # Read the preprocessed file
        with open(preprocessed_path, "rb") as file:
            preprocessed_file = file.read()

    return preprocessed_path, preprocessed_file

def convert_webm_to_mp4(input_file_path):
    # Create a temporary directory to store the converted file
    with tempfile.TemporaryDirectory() as temp_dir:
        # Generate output filename
        output_filename = os.path.splitext(os.path.basename(input_file_path))[0] + ".mp4"
        output_path = os.path.join(temp_dir, output_filename)

        # Convert WebM to MP4
        cap = cv2.VideoCapture(input_file_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            video_writer.write(frame)

        cap.release()
        video_writer.release()

        # Read the converted file
        with open(output_path, "rb") as file:
            converted_file = file.read()

    return output_filename, converted_file

def main():
    st.title("WebM to MP4 Converter")

    # Sidebar for file upload
    st.sidebar.header("Upload WebM File")
    uploaded_file = st.sidebar.file_uploader("Choose a WebM file", type=["webm"])

    # Main canvas
    if uploaded_file is not None:
        st.write("File uploaded: ", uploaded_file.name)
        
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name

        # Convert button
        if st.button("Convert to MP4"):
            try:
                # Preprocess the file
                with st.spinner("Preprocessing WebM file..."):
                    preprocessed_path, preprocessed_file = preprocess_webm(temp_file_path)

                # Convert the preprocessed file
                with st.spinner("Converting WebM to MP4..."):
                    output_filename, converted_file = convert_webm_to_mp4(preprocessed_path)

                # Remove the temporary files
                os.unlink(temp_file_path)
                os.unlink(preprocessed_path)

                # Display download button for the converted file
                st.success("Conversion completed!")
                st.download_button(
                    label="Download MP4",
                    data=converted_file,
                    file_name=output_filename,
                    mime="video/mp4"
                )

                # Display video player
                st.video(converted_file)

            except Exception as e:
                st.error(f"An error occurred during conversion: {e}")

    else:
        st.info("Please upload a WebM file using the sidebar.")

if __name__ == "__main__":
    main()
