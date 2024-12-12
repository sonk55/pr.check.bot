<template>
  <div class="dashboard">
    <header class="header">
      <h1>PR Monitoring Dashboard</h1>
      <div class="user-info">
        <router-link to="/admin/settings" class="settings-btn">Settings</router-link>
        <span>Welcome, Admin</span>
        <button @click="logout" class="logout-btn">Logout</button>
      </div>
    </header>

    <div class="stats-container">
      <div class="stat-card">
        <h3>Open PRs</h3>
        <div class="stat-number">{{ openPRs }}</div>
      </div>
      <div class="stat-card">
        <h3>In Review</h3>
        <div class="stat-number">{{ reviewPRs }}</div>
      </div>
      <div class="stat-card">
        <h3>Merged Today</h3>
        <div class="stat-number">{{ mergedToday }}</div>
      </div>
    </div>

    <div class="filters">
      <input 
        type="text" 
        v-model="search" 
        placeholder="Search PRs..." 
        class="search-input"
      >
      <select v-model="statusFilter" class="status-filter">
        <option value="">All Status</option>
        <option value="open">Open</option>
        <option value="review">In Review</option>
        <option value="merged">Merged</option>
      </select>
    </div>

    <div class="pr-list">
      <table>
        <thead>
          <tr>
            <th>PR #</th>
            <th>Title</th>
            <th>Author</th>
            <th>Status</th>
            <th>Updated</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pr in filteredPRs" :key="pr.id" :class="{'highlight': pr.isUrgent}">
            <td>{{ pr.number }}</td>
            <td>
              <div class="pr-title">
                {{ pr.title }}
                <span v-if="pr.isUrgent" class="urgent-tag">Urgent</span>
              </div>
            </td>
            <td>
              <div class="author">
                <img :src="pr.authorAvatar" :alt="pr.author" class="avatar">
                <span>{{ pr.author }}</span>
              </div>
            </td>
            <td><span :class="['status', pr.status]">{{ pr.status }}</span></td>
            <td>{{ formatDate(pr.updatedAt) }}</td>
            <td>
              <button class="action-btn">View</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PrDashboard',
  data() {
    return {
      search: '',
      statusFilter: '',
      pullRequests: [
        { 
          id: 1, 
          number: '#123', 
          title: 'Feature: Add new API endpoint', 
          author: 'john_doe',
          authorAvatar: 'https://avatars.githubusercontent.com/u/1?v=4',
          status: 'open', 
          updatedAt: '2023-12-01',
          isUrgent: true
        },
        { 
          id: 2, 
          number: '#124', 
          title: 'Fix: Memory leak issue', 
          author: 'jane_smith',
          authorAvatar: 'https://avatars.githubusercontent.com/u/2?v=4',
          status: 'review', 
          updatedAt: '2023-12-02'
        },
        // Add more mock data here
      ]
    }
  },
  computed: {
    filteredPRs() {
      return this.pullRequests.filter(pr => {
        const matchesSearch = pr.title.toLowerCase().includes(this.search.toLowerCase());
        const matchesStatus = !this.statusFilter || pr.status === this.statusFilter;
        return matchesSearch && matchesStatus;
      });
    },
    openPRs() {
      return this.pullRequests.filter(pr => pr.status === 'open').length;
    },
    reviewPRs() {
      return this.pullRequests.filter(pr => pr.status === 'review').length;
    },
    mergedToday() {
      return this.pullRequests.filter(pr => pr.status === 'merged').length;
    }
  },
  methods: {
    formatDate(date) {
      return new Date(date).toLocaleDateString();
    },
    logout() {
      this.$store.commit('setLoggedIn', false);
      localStorage.removeItem('isLoggedIn');
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logout-btn {
  padding: 0.5rem 1rem;
  background-color: #ff4757;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  text-align: center;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.search-input, .status-filter {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 200px;
}

table {
  width: 100%;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  overflow: hidden;
}

th {
  background-color: #f8f9fa;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
}

td {
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.pr-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.urgent-tag {
  background-color: #ff4757;
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.author {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
}

.status {
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  font-size: 0.9em;
  font-weight: 500;
}

.status.open {
  background-color: #e3f2fd;
  color: #1976d2;
}

.status.review {
  background-color: #fff3e0;
  color: #f57c00;
}

.status.merged {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.action-btn {
  padding: 0.5rem 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.highlight {
  background-color: #fff8e1;
}

.settings-btn {
  padding: 0.5rem 1rem;
  background-color: #4a90e2;
  color: white;
  border-radius: 4px;
  text-decoration: none;
  margin-right: 1rem;
}

@media (max-width: 768px) {
  .stats-container {
    grid-template-columns: 1fr;
  }
  
  .filters {
    flex-direction: column;
  }
  
  table {
    display: block;
    overflow-x: auto;
  }
}
</style>
