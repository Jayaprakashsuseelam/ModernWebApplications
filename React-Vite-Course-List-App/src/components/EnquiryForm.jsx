// src/components/EnquiryForm.js
import React, { useState } from 'react';
import axios from 'axios';

const EnquiryForm = ({ course, onClose }) => {
  const [form, setForm] = useState({ name: '', email: '' });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const data = { ...form, courseId: course.id, courseName: course.name };
    axios.post('http://localhost:5000/enquiries', data)
      .then(() => {
        alert('Enquiry submitted!');
        onClose();
      });
  };

  return (
    <form onSubmit={handleSubmit}>
      <h4>Enquire about {course.name}</h4>
      <input name="name" placeholder="Your Name" onChange={handleChange} required /><br />
      <input name="email" placeholder="Your Email" onChange={handleChange} required /><br />
      <button type="submit">Submit</button>
      <button onClick={onClose} type="button">Cancel</button>
    </form>
  );
};

export default EnquiryForm;
