<template>
  <section class="section">
    <div class="container">
      <h1 class="title">Mini Blog</h1>

      <b-field label="Title">
        <b-input v-model="newPost.title" placeholder="Enter title" />
      </b-field>

      <b-field label="Content">
        <b-input v-model="newPost.content" placeholder="Enter content" type="textarea" />
      </b-field>

      <b-button type="is-primary" @click="addPost">Create Post</b-button>

      <hr />

      <div v-if="posts.length === 0">No posts available</div>

      <b-card
          v-for="post in posts"
          :key="post.id"
          :title="post.title"
          class="mb-4"
      >
        <div class="content">{{ post.content }}</div>
        <b-button type="is-danger" @click="deletePost(post.id)">Delete</b-button>
      </b-card>
    </div>
  </section>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      posts: [],
      newPost: {
        title: '',
        content: ''
      },
      apiBase: 'https://myblog-api.onrender.com'
    };
  },
  methods: {
    async fetchPosts() {
      const res = await axios.get(`${this.apiBase}/posts`);
      this.posts = res.data;
    },
    async addPost() {
      if (!this.newPost.title || !this.newPost.content) return;

      const res = await axios.post(`${this.apiBase}/posts`, this.newPost);
      this.posts.push(res.data);
      this.newPost.title = '';
      this.newPost.content = '';
    },
    async deletePost(id) {
      await axios.delete(`${this.apiBase}/posts/${id}`);
      this.posts = this.posts.filter(post => post.id !== id);
    }
  },
  mounted() {
    this.fetchPosts();
  }
};
</script>
