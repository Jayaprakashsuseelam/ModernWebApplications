// src/components/Enquiries.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Enquiries = () => {
  const [enquiries, setEnquiries] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/enquiries')
      .then(res => setEnquiries(res.data));
  }, []);

  return (
    <div>
      <h2>All Enquiries</h2>
      {enquiries.map((enq, index) => (
        <div key={index} style={{ border: '1px dashed gray', marginBottom: '10px', padding: '10px' }}>
          <p><strong>Name:</strong> {enq.name}</p>
          <p><strong>Email:</strong> {enq.email}</p>
          <p><strong>Course:</strong> {enq.courseName}</p>
        </div>
      ))}
    </div>
  );
};

export default Enquiries;
