const ap = new APlayer({
    container: document.getElementById('aplayer'),
    fixed: true,
	autoplay: false, //自动播放
	listFolded: true, //列表默认折叠
	//lrcType: 3, //歌词传递方式
	mutex: true,
    audio: [
	{
        name: "浴室",
        artist: 'deca joins',
        url: 'http://music.163.com/song/media/outer/url?id=483378334.mp3',
        cover: 'https://p1.music.126.net/byjfkEIOWI_RmxSKEWTPyw==/18910500486297525.jpg?param=200y200',
		
    },
	{
        name: "虎口脱险",
        artist: '老狼--张磊',
        url: 'https://www.ytmp3.cn/down/39217.mp3',
        cover: 'https://y.qq.com/music/photo_new/T002R300x300M000004SjPIR07AkG0.jpg?max_age=2592000',
    },
	{
		name: "唯一",
		artist: '告五人',
		url: 'http://www.ytmp3.cn/down/75603.mp3',
		cover: 'https://y.qq.com/music/photo_new/T002R300x300M000000P4Dod0GzRlM.jpg?max_age=2592000',
	},
	{
		name: "我的心里是满的",
		artist: '程璧',
		url: 'http://www.ytmp3.cn/down/47442.mp3',
		cover: 'https://y.qq.com/music/photo_new/T002R300x300M000000wnEGB2OnTNh.jpg?max_age=2592000',
	},
	{
		name: "三十岁的女人",
		artist: '赵雷',
		url: 'http://music.163.com/song/media/outer/url?id=29567191.mp3',
		cover: 'https://p2.music.126.net/PJNV84mjt_mDXEkxtjzB4w==/18957779486268444.jpg?param=130y130',
	},
	]
});