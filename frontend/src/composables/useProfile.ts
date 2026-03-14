import { ref, watch } from 'vue'
import { API_BASE_URL } from '../config'
import type { UserProfile } from '../types/profile'

function createEmptyProfile(userId: string): UserProfile {
  return {
    user_id: userId,
    name: '',
    dob: '',
    gender: 'prefer_not_to_say',
    goal: 'improve_sleep',
    weight_lb: 0,
    height_cm: 0,
    preferred_workout_intensity: null,
    sleep_target_hours: null,
    notes: null,
  }
}

export function useProfile(selectedUserId: { value: string }) {
  const profile = ref<UserProfile>(createEmptyProfile(selectedUserId.value))
  const isLoading = ref(false)
  const isSaving = ref(false)
  const error = ref('')
  const successMessage = ref('')

  async function fetchProfile() {
    isLoading.value = true
    error.value = ''
    successMessage.value = ''

    try {
      const userId = selectedUserId.value
      const response = await fetch(`${API_BASE_URL}/user/profile/${userId}`)

      if (!response.ok) {
        throw new Error(`Failed to load profile: ${response.status}`)
      }

      const data: UserProfile = await response.json()
      profile.value = {
        ...data,
        preferred_workout_intensity: data.preferred_workout_intensity ?? null,
        sleep_target_hours: data.sleep_target_hours ?? null,
        notes: data.notes ?? null,
      }
    } catch (err) {
      profile.value = createEmptyProfile(selectedUserId.value)
      error.value =
        err instanceof Error ? err.message : 'Failed to load profile.'
    } finally {
      isLoading.value = false
    }
  }

  function validateProfile() {
    if (!profile.value.name.trim()) {
      error.value = 'Name is required.'
      return false
    }

    if (!profile.value.dob) {
      error.value = 'Date of birth is required.'
      return false
    }

    if (profile.value.weight_lb < 0 || Number.isNaN(profile.value.weight_lb)) {
      error.value = 'Weight must be a valid number.'
      return false
    }

    if (profile.value.height_cm < 0 || Number.isNaN(profile.value.height_cm)) {
      error.value = 'Height must be a valid number.'
      return false
    }

    if (
      profile.value.sleep_target_hours !== null &&
      (profile.value.sleep_target_hours < 4 ||
        profile.value.sleep_target_hours > 12)
    ) {
      error.value = 'Sleep target should be between 4 and 12 hours.'
      return false
    }

    return true
  }

  async function saveProfile() {
    error.value = ''
    successMessage.value = ''

    if (!validateProfile()) return

    isSaving.value = true

    try {
      const userId = selectedUserId.value

      const response = await fetch(`${API_BASE_URL}/user/profile/${userId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: profile.value.name,
          dob: profile.value.dob,
          gender: profile.value.gender,
          goal: profile.value.goal,
          weight_lb: profile.value.weight_lb,
          height_cm: profile.value.height_cm,
          preferred_workout_intensity: profile.value.preferred_workout_intensity,
          sleep_target_hours: profile.value.sleep_target_hours,
          notes: profile.value.notes,
        }),
      })

      if (!response.ok) {
        throw new Error(`Failed to save profile: ${response.status}`)
      }

      const updated: UserProfile = await response.json()
      profile.value = {
        ...updated,
        preferred_workout_intensity: updated.preferred_workout_intensity ?? null,
        sleep_target_hours: updated.sleep_target_hours ?? null,
        notes: updated.notes ?? null,
      }

      successMessage.value = 'Profile saved successfully.'
    } catch (err) {
      error.value =
        err instanceof Error ? err.message : 'Failed to save profile.'
    } finally {
      isSaving.value = false
    }
  }

  watch(
    () => selectedUserId.value,
    () => {
      profile.value = createEmptyProfile(selectedUserId.value)
      fetchProfile()
    },
    { immediate: true }
  )

  return {
    profile,
    isLoading,
    isSaving,
    error,
    successMessage,
    fetchProfile,
    saveProfile,
  }
}