<script setup lang="ts">
import { ref } from 'vue'
import { useProfile } from '../composables/useProfile'
import { USER_OPTIONS } from '../constants/users'

const selectedUserId = ref(USER_OPTIONS[0]?.user_id ?? '557975cf-2b37-4f1f-8d7e-0b80921d2db7')

const {
  profile,
  isLoading,
  isSaving,
  error,
  successMessage,
  saveProfile,
  fetchProfile,
} = useProfile(selectedUserId)
</script>

<template>
  <main class="profile-page">
    <section class="profile-header">
      <div>
        <h1>User Profile</h1>
        <p>Manage health preferences used for personalized recommendations.</p>
      </div>

      <button class="secondary-button" @click="fetchProfile">
        Reload
      </button>
    </section>

    <section class="user-picker-card">
      <label class="user-picker">
        <span>Select User</span>
        <select v-model="selectedUserId">
          <option
            v-for="user in USER_OPTIONS"
            :key="user.user_id"
            :value="user.user_id"
          >
            {{ user.name }}
          </option>
        </select>
      </label>
    </section>

    <section v-if="isLoading" class="state-box">
      Loading profile...
    </section>

    <section v-else class="profile-card">
      <div v-if="error" class="state-box error">{{ error }}</div>
      <div v-if="successMessage" class="state-box success">
        {{ successMessage }}
      </div>

      <form class="profile-form" @submit.prevent="saveProfile">
        <div class="form-grid">
          <label>
            <span>Name</span>
            <input v-model="profile.name" type="text" />
          </label>

          <label>
            <span>Date of Birth</span>
            <input v-model="profile.dob" type="date" />
          </label>

          <label>
            <span>Gender</span>
            <select v-model="profile.gender">
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
              <option value="prefer_not_to_say">Prefer not to say</option>
            </select>
          </label>

          <label>
            <span>Goal</span>
            <select v-model="profile.goal">
              <option value="improve_sleep">Improve sleep</option>
              <option value="fat_loss">Fat loss</option>
              <option value="endurance">Endurance</option>
              <option value="stress_reduction">Stress reduction</option>
            </select>
          </label>

          <label>
            <span>Weight (lb)</span>
            <input
              v-model.number="profile.weight_lb"
              type="number"
              min="0"
              step="0.1"
            />
          </label>

          <label>
            <span>Height (cm)</span>
            <input
              v-model.number="profile.height_cm"
              type="number"
              min="0"
              step="0.1"
            />
          </label>

          <label>
            <span>Preferred Workout Intensity</span>
            <select v-model="profile.preferred_workout_intensity">
              <option :value="null">Not set</option>
              <option value="low">Low</option>
              <option value="moderate">Moderate</option>
              <option value="high">High</option>
            </select>
          </label>

          <label>
            <span>Sleep Target (hours)</span>
            <input
              :value="profile.sleep_target_hours ?? ''"
              type="number"
              step="0.5"
              min="4"
              max="12"
              @input="
                profile.sleep_target_hours =
                  ($event.target as HTMLInputElement).value === ''
                    ? null
                    : Number(($event.target as HTMLInputElement).value)
              "
            />
          </label>
        </div>

        <label class="notes-field">
          <span>Notes</span>
          <textarea
            :value="profile.notes ?? ''"
            rows="5"
            placeholder="Add context like work schedule, recovery concerns, or goals..."
            @input="
              profile.notes =
                ($event.target as HTMLTextAreaElement).value || null
            "
          />
        </label>

        <div class="actions">
          <button class="primary-button" type="submit" :disabled="isSaving">
            {{ isSaving ? 'Saving...' : 'Save Profile' }}
          </button>
        </div>
      </form>
    </section>
  </main>
</template>

<style scoped>
.profile-page {
  max-width: 960px;
  margin: 0 auto;
  padding: 24px;
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 24px;
}

.profile-header h1 {
  margin: 0 0 8px 0;
}

.profile-header p {
  margin: 0;
  color: #666;
}

.user-picker-card {
    width: 25%;
    margin-bottom: 24px;
    padding: 0;
    color: #666;
}

label.user-picker {
  color: #E8E9ED;
}

.profile-card {
  background: white;
  color: #FFC759;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 1px 3px rgb(0 0 0 / 0.08);
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

label {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label span {
  font-size: 14px;
  font-weight: 600;
}

input,
select,
textarea {
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font: inherit;
  width: 100%;
  box-sizing: border-box;
}

textarea {
  resize: vertical;
}

.notes-field {
  width: 100%;
}

.actions {
  display: flex;
  justify-content: flex-end;
}

.primary-button,
.secondary-button {
  border: none;
  border-radius: 10px;
  padding: 10px 16px;
  cursor: pointer;
}

.primary-button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.state-box {
  padding: 14px;
  border-radius: 12px;
  margin-bottom: 16px;
  background: #f8fafc;
}

.state-box.error {
  background: #fee2e2;
  color: #666;
}

.state-box.success {
  background: #dcfce7;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .profile-header {
    flex-direction: column;
  }

  .actions {
    justify-content: stretch;
  }

  .primary-button {
    width: 100%;
  }
}
</style>