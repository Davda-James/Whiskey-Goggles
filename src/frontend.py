import gradio as gr
import io
import requests

# Define the keys in advance, as they are fixed
predefined_keys=["id","name","size","proof","abv","spirit_type","brand_id","popularity","image_url","avg_msrp","fair_price","shelf_price","total_score","wishlist_count","vote_count","bar_count","ranking","confidence_score"]									

def process_file(image, neighbors):
    if image is None:
        return "No image uploaded"

    # Convert the PIL Image to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="JPEG")  
    img_bytes.seek(0)  

    # Prepare the file for sending in the request
    files = {"file": ("uploaded.jpg", img_bytes, "image/jpeg")}

    params = {"neighbors": neighbors}

    # Send the image to the backend for processing
    response = requests.post("http://localhost:8000/predict", files=files, params=params)

    formatted_result = []
    # Handle the response
    if response.status_code == 200:
        
        result= response.json().get("result", None)
        if result is None:
            return f"<div class='result-wrapper'>{''.join(formatted_result)}</div>"
        for whiskey_results in result:
            for key in  predefined_keys:
                value = whiskey_results.get(key, None)
                if value is None:
                    whiskey_results[key] = "N/A"
                formatted_result.append(f"<div class='key-value'><span class='key'>{key}:</span><span class='value'>{value}</span></div>")
            formatted_result.append("<hr>")
        return f"<div class='result-wrapper'>{''.join(formatted_result)}</div>"
    else:
        for whiskey_results in result:
            for key in predefined_keys:
                formatted_result.append(f"<div class='key-value'><span class='key'>{key}:</span><span class='value'>Error</span></div>")
            formatted_result.append("<hr>")
        return f"<div class='result-wrapper'>{''.join(formatted_result)}</div>"


# Dark and light mode CSS
custom_css = """
#file-uploader {
    max-width: 100%;
    max-height: 300px; /* Limit height */
    object-fit: contain;
    border: 2px dashed #4A90E2;
    padding: 40px;
    text-align: center;
    font-size: 18px;
    background-color: #2c2c2c;
    color: #fff;
    border-radius: 12px;
    transition: border 0.3s ease;
}
.result-wrapper {
    max-height: 500px; /* Adjust height as needed */
    overflow-y: auto;
    padding: 10px;
    background-color: #1e1e1e;
    border: 1px solid #555;
    border-radius: 10px;
}
.result-block {
    max-height: 250px;
    overflow-y: auto;
    background-color: #1e1e1e;
    padding: 16px;
    margin-bottom: 12px;
    border-radius: 10px;
    border: 1px solid #444;
}

.key-value {
    display: flex;
    justify-content: space-between;
    margin-bottom: 6px;
    font-size: 15px;
    color: #ddd;
}

.key {
    font-weight: bold;
    margin-right: 8px;
    color: #00bcd4;
}

.value {
    flex-grow: 1;
    text-align: right;
    word-break: break-all; /* This will wrap long URLs */
    white-space: normal;   /* Allows it to wrap instead of staying in one line */
    overflow-wrap: anywhere; /* Extra safety for stubborn strings */
}
.result-block::-webkit-scrollbar {
    width: 6px;
}

.result-block::-webkit-scrollbar-thumb {
    background-color: #666;
    border-radius: 10px;
}
"""

def load_gradio():
    with gr.Blocks(css=custom_css) as demo:
        gr.HTML(
        """
        <div style="display: flex; align-items: center; justify-content: center;">
            <img src="https://res.cloudinary.com/dgvnuwspr/image/upload/v1740441389/wdqjosbtpgjiyi1ovups.png" style="height:60px; margin-right: 10px;">
            <h2 style="margin: 0; color: white;">Whiskey Bottle</h2>
        </div>
        """
    )   

        with gr.Row():
            with gr.Column():
                image_input = gr.Image(label="Uploaded Image",type="pil")
                # file_input = gr.File(
                #     file_types=[".jpeg", ".jpg",".png",".bmp", ".gif", ".tiff", ".webp"],
                #     label="📁 Upload Whisky Bottle File",
                #     elem_id="file-uploader"
                # 
                result_count = gr.Dropdown(
                    choices=[1, 2, 3, 4, 5],
                    value=1,
                    label="Select Number of Results",
                    interactive=True
                )
                submit_btn = gr.Button("🚀 Process", variant="primary")

            with gr.Column():
                output_text = gr.HTML(label="Whiskey Information", elem_id="output-text")
        submit_btn.click(fn=process_file, inputs=[image_input,result_count], outputs=output_text)

        # Custom CSS for rectangle-like styling
        demo.load(
            None,
            js=None,
        )

    demo.launch()



if __name__ == "__main__":
    load_gradio()



"""
#file-uploader {
    border: 2px dashed #4A90E2;
    padding: 40px;
    text-align: center;
    font-size: 18px;
    background-color: #f9f9f9;
    border-radius: 12px;
}
"""