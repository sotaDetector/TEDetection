<template>
  <div>
    <Select v-model="dsId">
      <Option v-for="item in dsList" :key="item.dsId" :value='item.dsId'>图片</Option>
      <!-- <Option :value=1>开启</Option> -->
    </Select>
  </div>
</template>

<script>
export default {
  data () {
    return {
      dsList: [],
      dsId: ''
    }
  },
  mounted () {
    this.getList()
  },
  methods: {
    getList () {
      let params = {}
      this.$Spin.show()
      this.$post('/dsc/getImageItemList', params).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {

        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
  }
}
</script>

<style lang="scss" scoped>
</style>