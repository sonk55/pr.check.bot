<template>
  <div class="admin-settings">
    <header class="header">
      <h1>Team Settings</h1>
      <button @click="addNewTeam" class="add-btn">Add New Team</button>
    </header>

    <div class="team-list">
      <div v-for="team in teams" :key="team" class="team-card">
        <div class="team-header">
          <h3>{{ team["name"] }}</h3>
          <div class="actions">
            <button @click="editTeam(team)" class="edit-btn">Edit</button>
            <button @click="deleteTeam(team)" class="delete-btn">Delete</button>
          </div>
        </div>
        <div class="team-details">
          <h4>Groups:</h4>
          <div v-for="group in teamGroups[team]" :key="group" class="group-item">
            <span>{{ group }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Team Modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h2>{{ isEditing ? 'Edit Team' : 'Add New Team' }}</h2>
        <form @submit.prevent="saveTeam">
          <div class="form-group">
            <label>Team Name:</label>
            <input v-model="editingTeam.name" :disabled="isEditing" required>
          </div>
          <div class="form-group">
            <label>Groups (comma-separated):</label>
            <input v-model="editingTeam.groups" required>
          </div>
          <div class="modal-actions">
            <button type="submit" class="save-btn">Save</button>
            <button type="button" @click="closeModal" class="cancel-btn">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminSettings',
  data() {
    return {
      teams: [],
      teamGroups: {},
      showModal: false,
      isEditing: false,
      editingTeam: {
        name: '',
        groups: ''
      }
    }
  },
  async created() {
    await this.loadTeams()
  },
  methods: {
    async loadTeams() {
      try {
        const response = await fetch('/api/teams')
        const data = await response.json()
        this.teams = data.teams
        
        // Load groups for each team
        for (const team of this.teams) {
          const groupResponse = await fetch(`/api/teams/${team["id"]}/groups`)
          const groupData = await groupResponse.json()
          this.teamGroups[team["id"]] = groupData.groups
        }
      } catch (error) {
        console.error('Error loading teams:', error)
      }
    },
    addNewTeam() {
      this.isEditing = false
      this.editingTeam = {
        name: '',
        groups: ''
      }
      this.showModal = true
    },
    editTeam(teamName) {
      this.isEditing = true
      this.editingTeam = {
        name: teamName,
        groups: this.teamGroups[teamName].join(',')
      }
      this.showModal = true
    },
    async deleteTeam(teamName) {
      if (confirm('Are you sure you want to delete this team?')) {
        try {
          // Note: Implement DELETE endpoint in server.py if needed
          const newTeams = this.teams.filter(t => t !== teamName)
          delete this.teamGroups[teamName]
          this.teams = newTeams
        } catch (error) {
          console.error('Error deleting team:', error)
        }
      }
    },
    async saveTeam() {
      try {
        // Note: Implement POST/PUT endpoints in server.py if needed
        if (!this.isEditing) {
          this.teams.push(this.editingTeam.name)
        }
        this.teamGroups[this.editingTeam.name] = this.editingTeam.groups.split(',').map(g => g.trim())
        this.closeModal()
      } catch (error) {
        console.error('Error saving team:', error)
      }
    },
    closeModal() {
      this.showModal = false
      this.editingTeam = {
        name: '',
        groups: ''
      }
    }
  }
}
</script>

<style scoped>
.admin-settings {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.add-btn {
  padding: 0.5rem 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.team-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.team-card {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.team-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.edit-btn, .delete-btn {
  padding: 0.25rem 0.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.edit-btn {
  background-color: #4a90e2;
  color: white;
}

.delete-btn {
  background-color: #ff4757;
  color: white;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 500px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
}

.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.save-btn, .cancel-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.save-btn {
  background-color: #42b983;
  color: white;
}

.cancel-btn {
  background-color: #666;
  color: white;
}

.group-item {
  background: #f5f7fa;
  padding: 0.5rem;
  margin: 0.25rem 0;
  border-radius: 4px;
}
</style>
