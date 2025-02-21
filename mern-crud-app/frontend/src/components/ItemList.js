import React, { useEffect, useState } from "react";
import axios from "axios";
import "./ItemList.css"; // Import CSS file for styling

const ItemList = ({ refreshTrigger }) => {
    const [items, setItems] = useState([]);

    useEffect(() => {
        fetchItems();
    }, [refreshTrigger]);

    const fetchItems = async () => {
        try {
            const response = await axios.get("http://localhost:5000/api/items");
            setItems(response.data);
        } catch (error) {
            console.error("Error fetching items:", error);
        }
    };

    return (
        <div className="table-container">
            <h2>Item List</h2>
            <table className="styled-table">
                <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Actions</th>
                </tr>
                </thead>
                <tbody>
                {items.length > 0 ? (
                    items.map((item) => (
                        <tr key={item._id}>
                            <td>{item._id}</td>
                            <td>{item.name}</td>
                            <td>
                                <button className="edit-btn" onClick={() => window.editItem(item)}>Edit</button>
                                <button className="delete-btn" onClick={() => window.deleteItem(item._id)}>Delete</button>
                            </td>
                        </tr>
                    ))
                ) : (
                    <tr>
                        <td colSpan="3" className="no-data">No items found.</td>
                    </tr>
                )}
                </tbody>
            </table>
        </div>
    );
};

export default ItemList;
