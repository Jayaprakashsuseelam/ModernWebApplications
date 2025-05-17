  // src/components/CourseList.jsx
  import React, { useEffect, useState } from 'react';
  import axios from 'axios';
  import EnquiryForm from './EnquiryForm.jsx';
  
  const CourseList = () => {
    const [courses, setCourses] = useState([]);
    const [selectedCourse, setSelectedCourse] = useState(null);
  
    useEffect(() => {
      axios.get('http://localhost:5000/courses')
        .then(res => setCourses(res.data));
    }, []);
  
    return (
      <div>
        <h2>Courses</h2>
        {courses.map(course => (
          <div key={course.id} style={{ border: '1px solid #ccc', marginBottom: '10px', padding: '10px' }}>
            <h3>{course.name}</h3>
            <p>{course.description}</p>
            <button onClick={() => setSelectedCourse(course)}>Enquire</button>
          </div>
        ))}
        {selectedCourse && (
          <EnquiryForm course={selectedCourse} onClose={() => setSelectedCourse(null)} />
        )}
      </div>
    );
  };
  
  export default CourseList;