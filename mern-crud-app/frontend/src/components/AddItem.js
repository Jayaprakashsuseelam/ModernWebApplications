import React, { useState } from "react";
import axios from "axios";

const AddItem = ({ onItemAdded }) => {
    const [name, setName] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post("http://localhost:5000/api/items", { name });
            setName("");
            onItemAdded(); // Trigger refresh
        } catch (error) {
            console.error("Error adding item:", error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter item name"
                required
            />
            <button type="submit">Add Item</button>
        </form>
    );
};

export default AddItem;
