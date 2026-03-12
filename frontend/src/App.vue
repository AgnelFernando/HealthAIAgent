<template>
  <div class="main">
    <nav class="nav-bar">
      <router-link to="/">Chat</router-link>
      <router-link to="/dashboard">Dashboard</router-link>
      <router-link to="/profile">Profile</router-link>
      <router-link to="/history">History</router-link>
    </nav>

    <div class="body">
      <router-view />
    </div>
    
  </div>
</template>

<style>
.main {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.nav-bar
 {
  display: flex;
  gap: 20px;
  padding: 20px 40px;
}
</style>
