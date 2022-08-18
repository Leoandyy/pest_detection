// pages/testHomePage/testHomePage.js




Page({

    /**
     * 页面的初始数据
     */
    data: {

    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad(options) {

    },

    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady() {

    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow() {

    },

    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide() {

    },

    /**
     * 生命周期函数--监听页面卸载
     */
    onUnload() {

    },

    /**
     * 页面相关事件处理函数--监听用户下拉动作
     */
    onPullDownRefresh() {

    },

    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom() {

    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage() {

    },

    
    // 按钮点击
    jumpToHomePage(){
        var _this=this
        wx.chooseImage({
            count:1,
            sizeType:['compressed'],
            sourceType: ['album', 'camera'],
            success (res) {
            // tempFilePath可以作为img标签的src属性显示图片
            const tempFilePaths = res.tempFilePaths;
            const fileManager = wx.getFileSystemManager();
            const base64 = fileManager.readFileSync(tempFilePaths[0], 'base64');
            //   console.log('=============================', base64);
            console.log('转码成功')
            
            wx.request({
                url: 'https://aip.baidubce.com/rest/2.0/image-classify/v1/plant?access_token=24.27685e2ce3f93a976420a0416595c6b9.2592000.1660314712.282335-26324295', //仅为示例，并非真实的接口地址
                method: 'post',
                data: {
                    "image":  base64
                },
                header: {
                    'content-type': 'application/x-www-form-urlencoded' // 默认值
                },
                success: (res) =>{
                    console.log(res.data)
                    _this.setData({
                        list: res.data,
                    })
                    wx.navigateTo({
                        url: '../showResult/showResult',
                    })
                }
            })
                
        },
        fail () {
            wx.showToast({
            title: '获取图片失败',
            icon: 'success',
            duration: 2000
            })
        }
        })
    }

})


        // wx.chooseImage({
        //     success (res) {
        //         // tempFilePath可以作为img标签的src属性显示图片
        //         const tempFilePaths = res.tempFilePaths;
        //         const fileManager = wx.getFileSystemManager();
        //         const base64 = fileManager.readFileSync(tempFilePaths[0], 'base64');
        //         //   console.log('=============================', base64);
        //         console.log('转码成功')
                
        //         wx.request({
        //             url: 'https://aip.baidubce.com/rest/2.0/image-classify/v1/plant?access_token=24.31a9e002747ba408263456ea5116ffb3.2592000.1656154520.282335-26324295', //仅为示例，并非真实的接口地址
        //             method: 'post',
        //             data: {
        //                 "image":  base64
        //             },
        //             header: {
        //                 'content-type': 'application/x-www-form-urlencoded' // 默认值
        //             },
        //             success (res) {
        //             console.log(res.data)
        //             }
        //         })
                    
        //     },
        //     fail () {
        //       wx.showToast({
        //         title: '获取图片失败',
        //         icon: 'success',
        //         duration: 2000
        //       })
        //     }
        //   })


            // success (res) {
            //     // tempFilePath可以作为img标签的src属性显示图片
            //     const tempFilePaths = res.tempFilePaths;
            //     wx.navigateTo({
            //         url: '../showResult/showResult?tempFilePaths='+tempFilePaths,
            //     })
            // },
            // fail () {
            //     wx.showToast({
            //     title: '获取图片失败',
            //     icon: 'success',
            //     duration: 2000
            //     })
            // }