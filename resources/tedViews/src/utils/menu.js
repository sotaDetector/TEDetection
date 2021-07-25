export const menuList = [{
  menuId: 1,
  menuName: '数据管理',
  url: '',
  ico: 'ios-analytics',
  children: [{
    menuId: 2,
    menuName: '数据集管理',
    url: 'dataManage',
    ico: 'ios-crop',
  },
  // {
  //   menuId: 3,
  //   menuName: '数据标注',
  //   url: 'markData'
  // }
]
},{
  menuId: 4,
  menuName: '模型管理',
  url: '',
  ico: 'ios-cube',
  children: [{
    menuId: 5,
    menuName: '模型管理',
    url: 'modelManage',
    ico: 'ios-cube-outline',
  }]
},{
  menuId: 6,
  menuName: '模型调用',
  url: '',
  ico: 'ios-hammer',
  children: [
    {
      menuId: 7,
      menuName: '检测服务',
      url: 'detectService',
      ico: 'ios-image-outline',
    },{
      menuId: 8,
      menuName: '检测任务',
      url: 'detectTask',
      ico: 'ios-videocam-outline',
    },
  //   {
  //   menuId: 7,
  //   menuName: '图片检测',
  //   url: 'imgDetect',
  //   ico: 'ios-image-outline',
  // },{
  //   menuId: 8,
  //   menuName: '视频检测',
  //   url: 'videoDetect',
  //   ico: 'ios-film-outline',
  // },{
  //   menuId: 9,
  //   menuName: '视频流检测',
  //   url: 'flowDetect',
  //   ico: 'ios-videocam-outline',
  // }
]
}]