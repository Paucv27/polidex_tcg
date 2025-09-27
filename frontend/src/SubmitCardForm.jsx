import React, {useState} from "react"

const SubmitCardFrom = ({}) => {

    const [preview, setPreview] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);

    const handleImageChange = (e) => {

        const file = e.target.files[0];
        if (file) {
            setSelectedFile(file);
            setPreview(URL.createObjectURL(file));
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!selectedFile) {
            alert("Please select a file first!!");
            return;
        } 

        const formData = new FormData();
        formData.append('image', selectedFile);

        console.log("Submitted card to Polidex - Awaiting response...")

        const response = await fetch('http://localhost:5000/process-image', {
            method: 'POST',
            body: formData,
        });

        const text = await response.text();
        console.log("Raw response text:", text);

        try {
            const result = JSON.parse(text);
            console.log("Parsed JSON:", result);

            // TODO display results with html to allow user to check their card stats and the listings they were extracted from (currently 5, should get larger samples later on)
            // TODO prompt user for accuracy feedback (simple accuracy meter + optional text)
        } catch(e) { 
            console.error("Failed to parse JSON:", e);
        }
    };


    return <div className="form-container">

        <form onSubmit={handleSubmit}>
            <label htmlFor="card_image">Select a card</label>
            <input 
                type="file" 
                id="image" 
                name="image" 
                accept="image/*" 
                capture="environment" 
                onChange={handleImageChange}
            />
            <button type="submit">Upload image</button>
        </form>
        {preview && (
            <div>
                <h4>Preview of your image</h4>
                <img src={preview} alt="preview" style={{maxWidth: "300px"}}/>
            </div>
        )}

    </div>
};

export default SubmitCardFrom;
