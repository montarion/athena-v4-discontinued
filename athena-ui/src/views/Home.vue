<template>
  <div class="home">
    <div class="main">
      <h1 class="title">Welcome to Athena</h1>
      <div class="content">
        <div class="card">
          <img
            class="image"
            src="https://cdn.sketchrepo.com/images/2x/d98b880f-9fef-46b5-a52b-5aceca8cef33.png"
          />
        </div>
        <div class="card">
          <img
            class="image"
            src="https://cdn.sketchrepo.com/images/2x/d98b880f-9fef-46b5-a52b-5aceca8cef33.png"
          />
        </div>
        <div class="card">
          <img
            class="image"
            src="https://cdn.sketchrepo.com/images/2x/d98b880f-9fef-46b5-a52b-5aceca8cef33.png"
          />
        </div>
        <div class="card">
          <img
            class="image"
            src="https://cdn.sketchrepo.com/images/2x/d98b880f-9fef-46b5-a52b-5aceca8cef33.png"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
// import Navbar from "@/components/Navbar";
export default {
  name: "Home",
  components: {
    // 'navbar': Navbar
  }
};
</script>

<style scoped lang="scss">
.subtitle {
  margin: 0;
  padding: 0;
  color: white;
  font-weight: 600;
  // border:
}
.image {
  width: 100%;
  height: 100%;
  overflow: hidden;
  border-radius: inherit;
}
.card {
  background-color: #2C3233;
  background-repeat: no-repeat;
  flex-basis: 40%;
  min-height: 15em;
  max-height: 15em;
  border-radius: 2em;
  margin-top: 2em;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.content {
  display: flex;
  flex-wrap: wrap;
  flex-grow: 1;
  justify-content: space-evenly;
}
.title {
  color: white;
}
</style>
