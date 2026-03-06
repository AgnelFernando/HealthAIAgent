<template>
  <div>
    <nav>
      <router-link to="/">Chat</router-link>
      <router-link to="/dashboard">Dashboard</router-link>
      <router-link to="/profile">Profile</router-link>
      <router-link to="/history">History</router-link>
    </nav>

    <router-view />
  </div>
</template>

<style>
nav {
  display: flex;
  gap: 20px;
  padding: 20px;
}
</style>