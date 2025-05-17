<template>
  <v-app theme="dark">
    <v-container class="py-8">
      <v-row>
        <!-- Header Section -->
        <v-col cols="12">
          <div class="text-center mb-8">
            <h1 class="text-h2 font-weight-bold gradient-text mb-2">SimpleStack Devlog</h1>
            <div class="text-subtitle-1 text-medium-emphasis">Share your thoughts with the world</div>
          </div>
        </v-col>

        <!-- Create Post Section - Left Column -->
        <v-col cols="12" md="6">
          <v-card class="mb-8 create-post-card sticky-card" elevation="4">
            <v-card-title class="text-h5 pa-4">Create New Post</v-card-title>
            <v-card-text>
              <v-form ref="createForm" v-model="createFormValid">
                <v-text-field
                  v-model="newPost.title"
                  label="Title"
                  placeholder="Enter title"
                  variant="outlined"
                  class="mb-4"
                  bg-color="surface"
                  color="primary"
                  :rules="titleRules"
                  :error-messages="newPost.titleError"
                  @input="validateField('title', newPost.title)"
                ></v-text-field>

                <v-textarea
                  v-model="newPost.content"
                  label="Content"
                  placeholder="Enter content"
                  variant="outlined"
                  class="mb-4"
                  bg-color="surface"
                  color="primary"
                  :rules="contentRules"
                  :error-messages="newPost.contentError"
                  @input="validateField('content', newPost.content)"
                  rows="4"
                ></v-textarea>

                <v-file-input
                  v-model="newPost.image"
                  label="Upload Image"
                  accept="image/*"
                  prepend-icon="mdi-camera"
                  class="mb-4"
                  @change="handleImagePreview"
                  bg-color="surface"
                  color="primary"
                  :rules="imageRules"
                  :error-messages="newPost.imageError"
                  @input="validateField('image', newPost.image)"
                ></v-file-input>

                <v-img
                  v-if="newPost.imagePreview"
                  :src="newPost.imagePreview"
                  max-height="200"
                  contain
                  class="mb-4 rounded-lg"
                ></v-img>

                <v-btn 
                  color="primary" 
                  @click="addPost" 
                  class="mb-2"
                  size="large"
                  block
                  :disabled="!createFormValid"
                >
                  Create Post
                </v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Blog Posts Section - Right Column -->
        <v-col cols="12" md="6">
          <div v-if="posts.length === 0" class="text-center text-body-1 text-medium-emphasis">
            No posts available. Be the first to create one!
          </div>

          <v-card
            v-for="post in posts"
            :key="post.id"
            class="mb-6 post-card"
            elevation="4"
          >
            <v-card-title class="pa-4">
              <template v-if="editingPost?.id === post.id">
                <v-form ref="editForm" v-model="editFormValid">
                  <v-text-field
                    v-model="editingPost.title"
                    label="Title"
                    variant="outlined"
                    density="compact"
                    class="mb-2"
                    bg-color="surface"
                    color="primary"
                    :rules="titleRules"
                    :error-messages="editingPost.titleError"
                    @input="validateField('title', editingPost.title, 'edit')"
                  ></v-text-field>
                </v-form>
              </template>
              <template v-else>
                <div class="text-h5 title-wrap">{{ post.title }}</div>
                <div class="text-caption text-medium-emphasis mt-1">
                  {{ new Date(post.created_at).toLocaleDateString() }}
                </div>
              </template>
            </v-card-title>
            <v-card-text class="pa-4">
              <template v-if="editingPost?.id === post.id">
                <v-textarea
                  v-model="editingPost.content"
                  label="Content"
                  variant="outlined"
                  density="compact"
                  class="mb-2"
                  bg-color="surface"
                  color="primary"
                  :rules="contentRules"
                  :error-messages="editingPost.contentError"
                  @input="validateField('content', editingPost.content, 'edit')"
                  rows="4"
                ></v-textarea>
                <v-file-input
                  v-model="editingPost.image"
                  label="Upload Image"
                  accept="image/*"
                  prepend-icon="mdi-camera"
                  class="mb-2"
                  @change="handleEditImagePreview"
                  bg-color="surface"
                  color="primary"
                  :rules="imageRules"
                  :error-messages="editingPost.imageError"
                  @input="validateField('image', editingPost.image, 'edit')"
                ></v-file-input>
                <v-img
                  v-if="editingPost.imagePreview"
                  :src="editingPost.imagePreview"
                  max-height="200"
                  contain
                  class="mb-2 rounded-lg"
                ></v-img>
              </template>
              <template v-else>
                <div class="text-body-1 mb-4">{{ post.content }}</div>
                <v-img
                  v-if="post.image_path"
                  :src="`${apiBase}${post.image_path}`"
                  max-height="300"
                  contain
                  class="rounded-lg"
                ></v-img>
              </template>
            </v-card-text>
            <v-card-actions class="pa-4">
              <template v-if="editingPost?.id === post.id">
                <v-btn 
                  color="success" 
                  @click="updatePost" 
                  class="me-2"
                  :disabled="!editFormValid"
                >
                  <v-icon start>mdi-content-save</v-icon>
                  Save
                </v-btn>
                <v-btn color="error" @click="cancelEdit" class="me-2">
                  <v-icon start>mdi-close</v-icon>
                  Cancel
                </v-btn>
              </template>
              <template v-else>
                <v-btn color="primary" @click="startEdit(post)" class="me-2">
                  <v-icon start>mdi-pencil</v-icon>
                  Edit
                </v-btn>
                <v-btn color="error" @click="deletePost(post.id)">
                  <v-icon start>mdi-delete</v-icon>
                  Delete
                </v-btn>
              </template>
            </v-card-actions>
          </v-card>
        </v-col>

        <!-- Technology Stack Section -->
        <v-col cols="12">
          <v-card class="mt-12 tech-stack-card" elevation="4">
            <v-card-title class="text-h5 pa-4">
              <v-icon start color="primary" class="me-2">mdi-code-tags</v-icon>
              Technology Stack Used
            </v-card-title>
            <v-card-text class="pa-4">
              <v-row>
                <v-col cols="12" sm="6" md="4">
                  <div class="tech-category mb-4">
                    <h3 class="text-h6 mb-3">Frontend</h3>
                    <div class="d-flex flex-wrap gap-2">
                      <v-chip
                        v-for="tech in frontendTech"
                        :key="tech.name"
                        :color="tech.color"
                        class="ma-1"
                        variant="elevated"
                      >
                        <v-icon start :icon="tech.icon" class="me-2"></v-icon>
                        {{ tech.name }}
                      </v-chip>
                    </div>
                  </div>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <div class="tech-category mb-4">
                    <h3 class="text-h6 mb-3">Backend</h3>
                    <div class="d-flex flex-wrap gap-2">
                      <v-chip
                        v-for="tech in backendTech"
                        :key="tech.name"
                        :color="tech.color"
                        class="ma-1"
                        variant="elevated"
                      >
                        <v-icon start :icon="tech.icon" class="me-2"></v-icon>
                        {{ tech.name }}
                      </v-chip>
                    </div>
                  </div>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <div class="tech-category mb-4">
                    <h3 class="text-h6 mb-3">Database</h3>
                    <div class="d-flex flex-wrap gap-2">
                      <v-chip
                        v-for="tech in databaseTech"
                        :key="tech.name"
                        :color="tech.color"
                        class="ma-1"
                        variant="elevated"
                      >
                        <v-icon start :icon="tech.icon" class="me-2"></v-icon>
                        {{ tech.name }}
                      </v-chip>
                    </div>
                  </div>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      posts: [],
      newPost: {
        title: '',
        content: '',
        image: null,
        imagePreview: null,
        titleError: '',
        contentError: '',
        imageError: ''
      },
      editingPost: null,
      apiBase: 'https://vue-expressapi-backend.onrender.com',
      createFormValid: false,
      editFormValid: false,
      titleRules: [
        v => !!v || 'Title is required',
        v => v.length >= 3 || 'Title must be at least 3 characters',
        v => v.length <= 100 || 'Title must be less than 100 characters'
      ],
      contentRules: [
        v => !!v || 'Content is required',
        v => v.length >= 10 || 'Content must be at least 10 characters',
        v => v.length <= 1000 || 'Content must be less than 1000 characters'
      ],
      imageRules: [
        v => !v || v.size < 2000000 || 'Image size should be less than 2 MB!',
        v => !v || /\.(jpeg|jpg|png|gif)$/.test(v.name) || 'Only image files are allowed!'
      ],
      // Technology Stack Data
      frontendTech: [
        { name: 'Vue.js', color: 'success', icon: 'mdi-vuejs' },
        { name: 'Vuetify', color: 'primary', icon: 'mdi-vuetify' },
        { name: 'Buefy', color: 'info', icon: 'mdi-buefy' },
        { name: 'Bulma', color: 'warning', icon: 'mdi-bulma' },
        { name: 'Axios', color: 'secondary', icon: 'mdi-axios' }
      ],
      backendTech: [
        { name: 'Node.js', color: 'success', icon: 'mdi-nodejs' },
        { name: 'Express', color: 'info', icon: 'mdi-express' },
        { name: 'Multer', color: 'warning', icon: 'mdi-upload' }
      ],
      databaseTech: [
        { name: 'SQLite', color: 'primary', icon: 'mdi-database' }
      ]
    };
  },
  methods: {
    validateField(field, value, mode = 'create') {
      const target = mode === 'create' ? this.newPost : this.editingPost;
      const rules = this[`${field}Rules`];
      
      for (const rule of rules) {
        const result = rule(value);
        if (result !== true) {
          target[`${field}Error`] = result;
          return false;
        }
      }
      
      target[`${field}Error`] = '';
      return true;
    },
    validateForm(mode = 'create') {
      const target = mode === 'create' ? this.newPost : this.editingPost;
      const fields = ['title', 'content', 'image'];
      
      return fields.every(field => this.validateField(field, target[field], mode));
    },
    async fetchPosts() {
      const res = await axios.get(`${this.apiBase}/posts`);
      this.posts = res.data;
    },
    handleImagePreview(file) {
      if (file && file instanceof File) {
        this.newPost.imagePreview = URL.createObjectURL(file);
      } else {
        this.newPost.imagePreview = null;
      }
    },
    handleEditImagePreview(file) {
      if (file && file instanceof File) {
        this.editingPost.imagePreview = URL.createObjectURL(file);
      } else {
        this.editingPost.imagePreview = null;
      }
    },
    async addPost() {
      if (!this.validateForm('create')) return;
      
      const formData = new FormData();
      formData.append('title', this.newPost.title);
      formData.append('content', this.newPost.content);
      if (this.newPost.image) {
        formData.append('image', this.newPost.image);
      }
      
      try {
        await axios.post(`${this.apiBase}/posts`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        
        this.newPost.title = '';
        this.newPost.content = '';
        this.newPost.image = null;
        this.newPost.imagePreview = null;
        this.newPost.titleError = '';
        this.newPost.contentError = '';
        this.newPost.imageError = '';
        
        await this.fetchPosts();
      } catch (error) {
        console.error('Error creating post:', error);
      }
    },
    async deletePost(id) {
      try {
        await axios.delete(`${this.apiBase}/posts/${id}`);
        await this.fetchPosts();
      } catch (error) {
        console.error('Error deleting post:', error);
      }
    },
    startEdit(post) {
      this.editingPost = { 
        ...post,
        image: null,
        imagePreview: null,
        titleError: '',
        contentError: '',
        imageError: ''
      };
    },
    cancelEdit() {
      this.editingPost = null;
    },
    async updatePost() {
      if (!this.validateForm('edit')) return;
      
      const formData = new FormData();
      formData.append('title', this.editingPost.title);
      formData.append('content', this.editingPost.content);
      if (this.editingPost.image) {
        formData.append('image', this.editingPost.image);
      }
      
      try {
        await axios.put(`${this.apiBase}/posts/${this.editingPost.id}`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        
        this.editingPost = null;
        await this.fetchPosts();
      } catch (error) {
        console.error('Error updating post:', error);
      }
    }
  },
  mounted() {
    this.fetchPosts();
  }
};
</script>

<style>
.gradient-text {
  background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.create-post-card {
  background: linear-gradient(145deg, #1a1a1a, #2d2d2d);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.post-card {
  background: linear-gradient(145deg, #1a1a1a, #2d2d2d);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.2s ease-in-out;
}

.post-card:hover {
  transform: translateY(-2px);
}

.v-card {
  border-radius: 12px !important;
}

.v-btn {
  text-transform: none !important;
  letter-spacing: 0.5px;
}

.v-text-field .v-field__input {
  min-height: 44px;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.v-textarea .v-field__input {
  min-height: 100px;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.tech-stack-card {
  background: linear-gradient(145deg, #1a1a1a, #2d2d2d);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.tech-category {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 16px;
}

.gap-2 {
  gap: 8px;
}

.v-chip {
  font-weight: 500;
  letter-spacing: 0.5px;
}

.sticky-card {
  position: sticky;
  top: 24px;
}

@media (max-width: 960px) {
  .sticky-card {
    position: static;
  }
}

.title-wrap {
  word-wrap: break-word;
  white-space: pre-wrap;
  overflow-wrap: break-word;
  max-width: 100%;
}
</style>
