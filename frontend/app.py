import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
import io
import os

# --- Configuration ---
FASTAPI_URL = os.environ.get("FASTAPI_URL", "http://localhost:8000/detect/")

st.set_page_config(layout="wide", page_title="Human Detector Pro")

# --- PAGE STYLING (Optional) ---
st.markdown("""
<style>
.stApp { 
    /* background-color: #f0f2f6; */ /* Light gray background - uncomment to use */
}
.stSuccess {
    background-color: #e6ffed;
    border-left: 5px solid #4CAF50;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("🧍 Human Detection Pro")
st.markdown("Welcome! Upload an image of a road scene, and this app will detect humans using a YOLO model.")
st.markdown("---_") # Creates a horizontal line

# --- UI Elements in Sidebar ---
st.sidebar.header("Controls")
confidence_threshold = st.sidebar.slider(
    "🎯 Confidence Threshold", 
    min_value=0.0, 
    max_value=1.0, 
    value=0.35,  # Default value
    step=0.01,
    help="Adjust the minimum confidence for a detection to be shown. Lower values show more (possibly uncertain) detections."
)
st.sidebar.markdown("---_")
uploaded_file = st.sidebar.file_uploader(
    "📂 Upload Image", type=["jpg", "jpeg", "png"]
)

# --- MAIN PANEL ---
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🖼️ Original Image")
        st.image(image, use_container_width=True)

    img_byte_arr = io.BytesIO()
    img_format = image.format if image.format else 'PNG'
    image.save(img_byte_arr, format=img_format)
    img_byte_arr = img_byte_arr.getvalue()

    with st.spinner('🧠 Analyzing image for humans...'):
        response_data = None
        try:
            files = {'file': (uploaded_file.name, img_byte_arr, uploaded_file.type)}
            response = requests.post(FASTAPI_URL, files=files, timeout=60)
            response.raise_for_status()
            response_data = response.json()
            
            detections = response_data.get("detections", [])
            image_with_detections = image.copy()
            draw = ImageDraw.Draw(image_with_detections)
            
            try:
                font = ImageFont.truetype("arial.ttf", 15) # Common font
            except IOError:
                font = ImageFont.load_default() # Fallback font

            num_filtered_detections = 0
            if detections:
                for det in detections:
                    if det['confidence'] >= confidence_threshold:
                        num_filtered_detections += 1
                        box = det['box']
                        label = f"{det['class_name']} ({det['confidence']:.2f})"
                        
                        outline_color = "#4CAF50"
                        text_fill_color = "#FFFFFF"
                        text_bg_color = "#4CAF50"

                        draw.rectangle(box, outline=outline_color, width=3)
                        
                        text_bbox = draw.textbbox((box[0], box[1]), label, font=font) 
                        text_width = text_bbox[2] - text_bbox[0]
                        text_height = text_bbox[3] - text_bbox[1]
                        
                        text_rect_y0 = box[1] - text_height - 4 # Position above box, with small padding
                        if text_rect_y0 < 0: # If text goes off top, position it below the box
                            text_rect_y0 = box[3] + 4
                        
                        # Ensure text background doesn't go out of image bounds (simplified check)
                        text_rect_x0 = max(0, box[0] - 2)
                        text_rect_y0_final = max(0, text_rect_y0)
                        text_rect_x1 = min(image_with_detections.width, box[0] + text_width + 4)
                        text_rect_y1 = min(image_with_detections.height, text_rect_y0_final + text_height + 4)
                        
                        draw.rectangle(
                            [text_rect_x0, text_rect_y0_final, text_rect_x1, text_rect_y1], 
                            fill=text_bg_color
                        )
                        draw.text((text_rect_x0 + 2, text_rect_y0_final + 2), label, font=font, fill=text_fill_color)

            with col2:
                st.subheader("🔍 Processed Image")
                st.image(image_with_detections, use_container_width=True)
                
                if num_filtered_detections == 1:
                    st.success(f"✅ Found {num_filtered_detections} human matching the criteria.")
                elif num_filtered_detections > 1:
                    st.success(f"✅ Found {num_filtered_detections} humans matching the criteria.")
                elif not detections:
                    st.warning("⚠️ Model made no detections in this image.")
                else:
                    st.info(
                        f"ℹ️ No humans detected above {confidence_threshold:.2f} confidence. "
                        "Try lowering the threshold in the sidebar."
                    )
            
            if st.sidebar.checkbox("⚙️ Show Raw JSON Output", False) and response_data:
                st.subheader("Raw Model Output (JSON)")
                st.json(response_data)

        except requests.exceptions.ConnectionError:
            st.error(
                f"Connection Error: Could not connect to the backend at {FASTAPI_URL}. "
                "Ensure the backend service is running and the URL is correct."
            )
        except requests.exceptions.Timeout:
            st.error(
                "Request Timeout: The backend took too long processing the image. "
                "This might be due to a large image or high server load."
            )
        except requests.exceptions.HTTPError as e:
            st.error(f"HTTP Error from Backend: {e.response.status_code}")
            try:
                error_detail = e.response.json().get("detail", "No additional details from backend.")
                st.error(f"Backend message: {error_detail}")
            except ValueError:
                st.text(f"Backend message (raw): {e.response.text}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
else:
    st.info("👋 Please upload an image using the sidebar to begin detection.")

st.sidebar.markdown("---_")
st.sidebar.markdown("Built with [Streamlit](https://streamlit.io) & [FastAPI](https://fastapi.tiangolo.com/).") 