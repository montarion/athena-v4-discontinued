<template>
  <div id="app">
    <div class="sidenav">
      <navbar />
    </div>
    <router-view />
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";
export default {
  name: "App",
  components: {
    navbar: Navbar
  }
};
</script>

<style lang="scss">

html {
 background-color: #14141E;
 color: white;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.v-sidebar-menu {
}
.v-sidebar-menu.vsm_expanded {
}
.v-sidebar-menu.vsm_collapsed {
}
.v-sidebar-menu.vsm_rtl {
}

// item row
.v-sidebar-menu .vsm--item {
}

.v-sidebar-menu .vsm--item.vsm--item_open {
}
.v-sidebar-menu .vsm--link {
  // box-shadow: 3px 0px 0px 0px #1756bb inset;
}
.v-sidebar-menu .vsm--link.vsm--link_active {
  background-color: #2c3e50;
  box-shadow: 3px 0px 0px 0px #1756bb inset !important;

  // rgb(162, 0, 255)
}
.v-sidebar-menu .vsm--link.vsm--link_exact-active {
}
.v-sidebar-menu .vsm--link.vsm--link_mobile-item {
}
.v-sidebar-menu .vsm--link.vsm--link_level-[n] {
}
.v-sidebar-menu .vsm--link.vsm--link_disabled {
}
.v-sidebar-menu .vsm--title {
}
.v-sidebar-menu .vsm--icon {
}
.v-sidebar-menu .vsm--arrow {
}
.v-sidebar-menu .vsm--arrow.vsm--arrow_open {
}
.v-sidebar-menu .vsm--badge {
}
.v-sidebar-menu .vsm--header {
  color: #4285f4 !important;
}
.v-sidebar-menu .vsm--list {
}
.v-sidebar-menu .vsm--dropdown > .vsm--list {
}
.v-sidebar-menu .vsm--mobile-item {
}
.v-sidebar-menu .vsm--mobile-bg {
}
.v-sidebar-menu .vsm--toggle-btn {
}
</style>
