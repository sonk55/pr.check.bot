<template>
  <div class="login-container">
    <form @submit.prevent="handleLogin" class="login-form">
      <h2>Admin Login</h2>
      <div class="form-group">
        <input type="text" v-model="username" placeholder="Username" required>
      </div>
      <div class="form-group">
        <input type="password" v-model="password" placeholder="Password" required>
      </div>
      <button type="submit">Login</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script>
export default {
  name: 'AdminLogin',
  data() {
    return {
      username: '',
      password: '',
      error: ''
    }
  },
  methods: {
    handleLogin() {
      // 실제 구현시에는 API 호출로 대체
      if (this.username === 'admin' && this.password === 'admin123') {
        this.$store.commit('setLoggedIn', true);
        localStorage.setItem('isLoggedIn', 'true');
        this.$router.push('/dashboard');
      } else {
        this.error = 'Invalid credentials';
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
.login-form {
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  width: 300px;
}
.form-group {
  margin-bottom: 1rem;
}
input {
  width: 100%;
  padding: 8px;
  margin: 8px 0;
  border: 1px solid #ddd;
  border-radius: 4px;
}
button {
  width: 100%;
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.error {
  color: red;
  font-size: 0.9em;
}
</style>
