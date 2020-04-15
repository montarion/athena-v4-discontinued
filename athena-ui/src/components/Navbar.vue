<template>
  <sidebar-menu
    :menu="menu"
    @toggle-collapse="onToggleCollapse"
    :collapsed="collapsed"
    :theme="theme"
    :disableHover="disableHover"
  >
    <!-- <div slot="header">header</div> -->
    <!-- <div slot="footer">footer</div> -->
    <span slot="toggle-icon">
      <font-awesome-icon icon="bars" />
    </span>
    <span slot="dropdown-icon">
      <font-awesome-icon icon="arrow-alt-circle-right" />
    </span>
  </sidebar-menu>
</template>

<script>
export default {
  props: {
    collapsed: {
      type: Boolean,
      default: true
    },
    // Sidebar theme (available themes: 'white-theme')
    theme: {
      type: String,
      default: ""
    },

    // Disable hover on collapse mode
    disableHover: {
      type: Boolean,
      default: false
    }
  },
  created: function() {
  },
  methods: {
    onToggleCollapse: function() { //(collapsedStateBool)
    }
  },
  data() {
    return {
      menu: [
        {
          header: true,
          title: "Athena V4",
          hiddenOnCollapse: true
        },
        {
          href: "/",
          icon: {
            element: "font-awesome-icon",
            attributes: { icon: "home" }
            // text: ''
          },
          title: "Home"
        },
        {
          icon: {
            element: "font-awesome-icon",
            attributes: { icon: "border-all" }
          },
          title: "Dashboard",
          child: [
            {
              href: "/anime",
              icon: {
                element: "font-awesome-icon",
                attributes: { icon: "dragon" }
                // text: ''
              },
              title: "Anime"
            },
            {
              href: "/motd",
              icon: {
                element: "font-awesome-icon",
                attributes: { icon: "bullhorn" }
                // text: ''
              },
              title: "MOTD"
            }
          ]
        }
      ]
    };
  }
};
</script>