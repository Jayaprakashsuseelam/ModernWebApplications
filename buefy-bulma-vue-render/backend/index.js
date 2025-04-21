const express = require('express');
const cors = require('cors');
const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

let posts = [
    { id: 1, title: 'Hello World', content: 'This is the first blog post' }
];

// Get all posts
app.get('/posts', (req, res) => {
    res.json(posts);
});

// Create a new post
app.post('/posts', (req, res) => {
    const { title, content } = req.body;
    const newPost = { id: Date.now(), title, content };
    posts.push(newPost);
    res.status(201).json(newPost);
});

// Delete a post
app.delete('/posts/:id', (req, res) => {
    const { id } = req.params;
    posts = posts.filter(post => post.id !== parseInt(id));
    res.status(204).send();
});

app.listen(PORT, () => {
    console.log(`API running on http://localhost:${PORT}`);
});
