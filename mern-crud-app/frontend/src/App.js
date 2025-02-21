import React, { useState } from "react";
import ItemList from "./components/ItemList";
import AddItem from "./components/AddItem";
import axios from "axios";
import "./App.css"; // Import global styles

function App() {
    const [refresh, setRefresh] = useState(0);

    window.editItem = (item) => {
        const newName = prompt("Edit Item Name:", item.name);
        if (newName) {
            axios.put(`http://localhost:5000/api/items/${item._id}`, { name: newName })
                .then(() => setRefresh((prev) => prev + 1))
                .catch((err) => console.error("Error updating item:", err));
        }
    };

    window.deleteItem = (id) => {
        if (window.confirm("Are you sure you want to delete this item?")) {
            axios.delete(`http://localhost:5000/api/items/${id}`)
                .then(() => setRefresh((prev) => prev + 1))
                .catch((err) => console.error("Error deleting item:", err));
        }
    };

    return (
        <div className="app-container">
            <h1>Real-Time MERN CRUD App</h1>
            <AddItem onItemAdded={() => setRefresh((prev) => prev + 1)} />
            <ItemList refreshTrigger={refresh} />
        </div>
    );
}

export default App;
