"""
Generate individual tool detail pages for all 110+ AI tools.
Each page: rich intro, features, pros/cons, use cases, pricing, similar tools, ads.
"""
import os, json, random, urllib.parse

TOOLS_DIR = os.path.join(os.path.dirname(__file__), "tools")
os.makedirs(TOOLS_DIR, exist_ok=True)
BASE_URL = "https://aitools-khaki.vercel.app"

# ---- Tool data with enriched info ----
tools = [
    # chat
    {"name":"ChatGPT","icon":"🤖","cat":"chat","cat_name":"对话聊天","url":"https://chat.openai.com","pricing":"免费版GPT-4o mini / Plus $20/月 / Pro $200/月","features":"多轮对话理解能力极强，支持GPT-4o多模态输入（图片/文件/语音），DALL·E图像生成，插件和GPTs生态丰富，代码解释器可做数据分析","merit":"综合能力最强,多模态支持全,插件生态最丰富","weakness":"高峰期响应慢,免费版有次数限制,国内需翻墙","scene":"适合几乎所有AI需求场景——写作、编程、学习、翻译、头脑风暴，是最通用的AI助手"},
    {"name":"Claude","icon":"🧠","cat":"chat","cat_name":"对话聊天","url":"https://claude.ai","pricing":"免费版有限额 / Pro $20/月 / Team $25/人/月","features":"200K超长上下文（一次可读整本书），Artifacts可交互式内容生成，代码生成和调试能力优秀，Project知识库管理，写作风格自然流畅","merit":"长文本处理最强,代码能力一流,语言自然不AI感","weakness":"国内需要翻墙,免费版限额较紧,不支持实时搜索","scene":"适合长篇报告撰写、学术论文分析、代码开发、复杂逻辑推理等深度工作"},
    {"name":"Gemini","icon":"🌐","cat":"chat","cat_name":"对话聊天","url":"https://gemini.google.com","pricing":"免费 / Advanced $19.99/月（含2TB Google One）","features":"Google搜索深度整合，YouTube/Gmail/地图等生态联动，Imagen多模态理解，支持超长上下文，免费用GPT-4级别能力","merit":"免费版能力强,Google生态整合,多模态理解好","weakness":"国内访问不便,中文不如国产模型","scene":"适合Google生态用户、需要实时信息检索的研究者、多模态内容分析"},
    {"name":"DeepSeek","icon":"🐋","cat":"chat","cat_name":"对话聊天","url":"https://chat.deepseek.com","pricing":"完全免费 / API极低价（约为GPT-4的1/50）","features":"开源模型能力对标GPT-4，数学推理和代码生成突出，支持超长上下文，中文理解自然流畅，API价格极低","merit":"完全免费,数学推理超强,API价格最低","weakness":"高峰期响应偏慢,联网功能有限","scene":"适合高性价比AI需求的学生、开发者、中小企业，推理和编程场景尤其出色"},
    {"name":"Kimi","icon":"🌙","cat":"chat","cat_name":"对话聊天","url":"https://kimi.moonshot.cn","pricing":"免费额度充足 / 会员制部分功能付费","features":"超长上下文文档分析，支持联网搜索和网页链接读取，中文长文写作流畅，文件格式支持多（PDF/Word/PPT/图片）","merit":"免费额度大,联网搜索好用,中文长文本强","weakness":"高峰期排队,长文生成偶有中断","scene":"适合日常写作、资料整理、新闻摘要、学生写作业等国内用户日常AI需求"},
    {"name":"通义千问","icon":"☁️","cat":"chat","cat_name":"对话聊天","url":"https://tongyi.aliyun.com","pricing":"免费 / 企业版按量计费","features":"阿里云大模型，整合钉钉/夸克/高德等阿里生态，写作翻译代码图像生成全覆盖，电商和办公场景优化深","merit":"免费,阿里生态整合好,场景覆盖广","weakness":"长文逻辑偶尔跑偏,单项能力非最优","scene":"适合阿里生态用户、钉钉办公场景、电商文案撰写、中文综合AI需求"},
    {"name":"文心一言","icon":"📘","cat":"chat","cat_name":"对话聊天","url":"https://yiyan.baidu.com","pricing":"免费 / 专业版会员制","features":"百度文心大模型，中文理解能力优秀，百度搜索数据训练，国产知识覆盖好，支持多模态生成","merit":"中文理解深厚,百度搜索整合,国产化适配好","weakness":"英文能力较弱,创意写作一般","scene":"适合中文为主的内容创作、知识问答、国内信息查询"},
    {"name":"豆包","icon":"🫘","cat":"chat","cat_name":"对话聊天","url":"https://www.doubao.com","pricing":"完全免费","features":"字节跳动AI助手，响应速度极快，手机端体验流畅，多端同步优秀，日常聊天写作翻译都够用","merit":"完全免费,速度飞快,多端体验好","weakness":"专业深度不够,创意能力偏弱","scene":"适合轻度AI用户、碎片化写作、快速查资料、日常助手"},
    {"name":"Perplexity","icon":"🔎","cat":"chat","cat_name":"对话聊天","url":"https://www.perplexity.ai","pricing":"免费 / Pro $20/月（支持GPT-4/Claude等多模型）","features":"AI搜索引擎开创者，答案带精确来源引用，支持多轮追问深挖，学术研究Copilot模式，可切换多种底层模型","merit":"答案带来源引用,学术搜索最强,多模型可选","weakness":"Pro版付费,英文内容多于中文","scene":"适合学术研究、事实核查、深度信息检索、替代传统搜索引擎"},
    {"name":"讯飞星火","icon":"🔥","cat":"chat","cat_name":"对话聊天","url":"https://xinghuo.xfyun.cn","pricing":"免费 / 企业版定制收费","features":"科大讯飞出品，语音识别和合成技术领先，多模态理解，编程数学写作多场景，教育/医疗等行业深耕","merit":"语音技术最强,行业解决方案丰富,国产可靠","weakness":"通用对话不如头部模型,认知能力中等","scene":"适合语音交互场景、教育行业、医疗等垂直领域AI应用"},
    {"name":"360智脑","icon":"🛡️","cat":"chat","cat_name":"对话聊天","url":"https://chat.360.com","pricing":"免费","features":"360出品大模型，搜索+AI深度融合，安全领域优势明显，中文内容理解好，PC端和移动端体验流畅","merit":"免费,安全能力强,搜索整合","weakness":"创意能力一般,国际竞争力弱","scene":"适合日常搜索、安全相关AI需求、国内普通用户"},
    {"name":"百川智能","icon":"🌊","cat":"chat","cat_name":"对话聊天","url":"https://www.baichuan-ai.com","pricing":"免费 / API收费","features":"王小川创立，百川大模型系列开源可商用，中文能力行业领先，医疗/法律等专业领域训练","merit":"开源可商用,中文优秀,专业领域强","weakness":"品牌认知度不如头部,生态待完善","scene":"适合企业私有化部署、专业领域AI应用、中文NLP开发"},
    {"name":"Poe","icon":"🦉","cat":"chat","cat_name":"对话聊天","url":"https://poe.com","pricing":"免费 / 订阅$19.99/月","features":"Quora出品，一站式使用ChatGPT/Claude/Gemini等多种AI模型，可自定义Bot，社区分享Bot生态","merit":"多模型一站式,免费可用主流模型,社区活跃","weakness":"高级功能需订阅,翻墙访问","scene":"适合想同时体验多个AI模型、不想分别注册各平台的用户"},
    {"name":"Character.AI","icon":"🎭","cat":"chat","cat_name":"对话聊天","url":"https://character.ai","pricing":"免费 / c.ai+ $9.99/月","features":"AI角色扮演开创者，可创建自定义人格的AI角色，对话沉浸感强，社区角色丰富（名人/动漫/助手等）","merit":"角色扮演最沉浸,角色库丰富,免费可用","weakness":"实用功能弱,不适合生产力场景","scene":"适合娱乐消遣、语言练习、创意写作灵感、角色扮演爱好者"},

    # image
    {"name":"Midjourney","icon":"🎨","cat":"image","cat_name":"图像创作","url":"https://www.midjourney.com","pricing":"Basic $10/月 / Standard $30/月 / Pro $60/月","features":"公认AI绘画质量天花板，V6/Raw模式画质细腻，风格参考/角色一致性功能，Discord社区创作交流，Remix模式无限变体","merit":"画质业界天花板,艺术感极强,社区活跃灵感多","weakness":"需付费,Discord操作有门槛,中文Prompt支持一般","scene":"适合对画面质量有极致要求的设计师、艺术家、品牌视觉创作"},
    {"name":"Stable Diffusion","icon":"🖼️","cat":"image","cat_name":"图像创作","url":"https://stability.ai","pricing":"开源免费 / 云服务按使用量","features":"完全开源可本地部署，ControlNet精确控制构图，LoRA/LyCORIS轻量微调风格，插件生态极丰富（ComfyUI/A1111），支持动画和视频","merit":"完全开源,可本地部署,可控性最强,插件最丰富","weakness":"需要显卡配置,学习成本高,出图需要调教","scene":"适合有技术基础、追求完全创作自由、需要批量定制化出图的专业用户"},
    {"name":"DALL·E 3","icon":"✨","cat":"image","cat_name":"图像创作","url":"https://openai.com/dall-e-3","pricing":"ChatGPT Plus包含 / API按量计费","features":"文字理解力最强的AI绘画，能精确按描述生成图像，与ChatGPT深度集成对话式生图，文字渲染准确率高，伦理安全过滤完善","merit":"文字理解力最强,对话式操作简单,细节精准","weakness":"需ChatGPT付费,风格不如MJ丰富,版权受限","scene":"适合不擅长写复杂Prompt、需要按精准描述出图的普通用户"},
    {"name":"Canva AI","icon":"🎯","cat":"image","cat_name":"图像创作","url":"https://www.canva.com","pricing":"免费 / Pro $12.99/月 / Teams $14.99/月","features":"Canva内置AI设计助手，Magic Media文生图/AI修图，海量模板+AI自动排版，品牌工具包统一视觉，协作分享功能完善","merit":"模板最丰富,零门槛上手,设计+AI一体化","weakness":"高级AI功能需Pro,纯绘画不如专业绘画工具","scene":"适合非设计师做专业视觉内容、自媒体运营、小型团队设计协作"},
    {"name":"Remove.bg","icon":"✂️","cat":"image","cat_name":"图像创作","url":"https://www.remove.bg","pricing":"免费（低清）/ 按张或订阅（高清）","features":"AI一键去除图片背景，5秒出结果，支持批量处理，API可集成到工作流，效果在同类产品中领先","merit":"抠图最快最准,操作极简,支持API","weakness":"高清需付费,只做抠图功能单一","scene":"适合电商产品图处理、证件照换底、社交媒体图片快速去背景"},
    {"name":"Leonardo.AI","icon":"🎮","cat":"image","cat_name":"图像创作","url":"https://leonardo.ai","pricing":"免费额度 / 订阅从$12/月起","features":"专注游戏资产和概念艺术生成，角色/场景设计专业，Alchemy优化画质，多种专业模型可选，社区图片风格参考","merit":"游戏概念设计最强,角色一致性好,模型丰富","weakness":"偏游戏风格,不适合写实摄影","scene":"适合游戏美术、概念设计师、动漫创作者、需要角色一致性生成的场景"},
    {"name":"Adobe Firefly","icon":"🔥","cat":"image","cat_name":"图像创作","url":"https://firefly.adobe.com","pricing":"免费额度 / Creative Cloud订阅含更多","features":"Adobe出品深耕创意设计，与Photoshop/Illustrator深度整合，生成式填充/扩展画布/文字特效，商用版权安全有保障","merit":"Adobe全家桶整合,商用版权安全,专业设计强","weakness":"纯绘画不如MJ,创作自由度受限","scene":"适合Adobe生态内设计师、需要商用安全AI图像的企业用户"},
    {"name":"通义万相","icon":"🖌️","cat":"image","cat_name":"图像创作","url":"https://tongyi.aliyun.com/wanxiang","pricing":"免费","features":"阿里推出的国产AI绘画，中文Prompt理解好，国风/二次元/插画等本土风格表现佳，文生图/图生图/风格转换全支持","merit":"免费,中文理解好,本土风格丰富","weakness":"写实风格不如MJ,出图质量有波动","scene":"适合国内用户日常作图、电商素材、社交媒体配图、国风创作"},
    {"name":"文心一格","icon":"🎨","cat":"image","cat_name":"图像创作","url":"https://yige.baidu.com","pricing":"免费额度大 / 高级功能会员","features":"百度文心大模型驱动的AI绘画，中文Prompt优化，支持国画/油画/水彩等多种艺术风格，百度搜索搜图+生图一站式","merit":"免费额度大,风格多样,本土艺术风格好","weakness":"复杂场景处理弱,细节精细度一般","scene":"适合需要大量配图的内容创作者、教育工作者、个人艺术爱好者"},
    {"name":"美图AI","icon":"📸","cat":"image","cat_name":"图像创作","url":"https://ai.meitu.com","pricing":"免费 / VIP功能付费","features":"美图秀秀AI矩阵，AI写真/AI绘画/AI扩图/AI消除，拍照修图一条龙，手机端体验极佳，女性用户群体大","merit":"拍照修图一体,手机端最优,操作极简","weakness":"专业级创作受限,偏消费级应用","scene":"适合日常拍照修图、社交媒体美颜、个人写真创作、电商产品图美化"},
    {"name":"Clipdrop","icon":"💡","cat":"image","cat_name":"图像创作","url":"https://clipdrop.co","pricing":"免费额度 / Pro订阅","features":"Stability AI出品，AI图像增强/修复/打光/超分辨率，Relight重新打光功能独特，一键去背景/去文字/放大","merit":"增强修复专业,打光功能独特,效果出色","weakness":"免费额度有限,功能偏工具型","scene":"适合电商产品图优化、老照片修复、专业级后期增强"},
    {"name":"SeaArt","icon":"🌊","cat":"image","cat_name":"图像创作","url":"https://www.seaart.ai","pricing":"免费额度 / 会员付费","features":"国产AI绘画平台，模型丰富（含二次元/写实/CG等多种风格），社区活跃可参考他人作品，新手引导好上手快","merit":"模型丰富,社区活跃,新手友好","weakness":"高端画质不如MJ,服务器偶尔拥挤","scene":"适合AI绘画入门、二次元创作、国内AI绘画爱好者社区交流"},
    {"name":"Upscale.media","icon":"🔍","cat":"image","cat_name":"图像创作","url":"https://www.upscale.media","pricing":"免费（低分辨率）/ 付费高清","features":"AI图片无损放大，支持2x/4x/8x放大倍数，保留细节不模糊，电商图优化利器，批量处理支持","merit":"放大效果好,操作简单,批量处理","weakness":"高清需付费,功能较单一","scene":"适合电商产品图放大、老照片/低分辨率图片增强"},

    # video
    {"name":"Sora","icon":"🎬","cat":"video","cat_name":"视频生成","url":"https://openai.com/sora","pricing":"ChatGPT Plus/Pro包含","features":"OpenAI视频生成模型，文字描述生成逼真视频，画面连贯性和物理合理性业界领先，支持多种画幅比例，视频时长和画质突出","merit":"画质和连贯性领先,物理理解力强","weakness":"尚未完全开放,生成时间长,资源消耗大","scene":"适合视频创意预演、概念验证、广告分镜制作、影视前期可视化"},
    {"name":"Runway","icon":"🎥","cat":"video","cat_name":"视频生成","url":"https://runwayml.com","pricing":"免费额度 / Standard $15/月 / Pro $35/月","features":"专业级AI视频平台，Gen-3/Gen-4模型持续更新，文生视频/图生视频/视频编辑，运动笔刷精准控制，绿幕/超分/插帧等工具","merit":"功能最全面,持续迭代,专业级工具","weakness":"价格偏高,学习曲线陡峭","scene":"适合专业视频制作人、广告公司、独立电影人、创意工作室"},
    {"name":"Pika","icon":"🍿","cat":"video","cat_name":"视频生成","url":"https://pika.art","pricing":"免费额度 / 订阅$10/月起","features":"轻量级AI视频生成，界面简洁易上手，支持Lip Sync口型同步，视频风格转换，社区模板分享，出图速度快","merit":"简单易用,出视频快,Lip Sync独特","weakness":"视频时长偏短,复杂场景表现一般","scene":"适合社交媒体短视频、个人创意表达、快速视频实验"},
    {"name":"可灵","icon":"⚡","cat":"video","cat_name":"视频生成","url":"https://kling.kuaishou.com","pricing":"免费额度 / 会员付费","features":"快手推出，国产AI视频生成领先者，文生视频/图生视频质量高，中文理解自然，运动幅度和画面质量国产最优","merit":"国产领先,视频质量好,中文Prompt","weakness":"生成时长有限,高峰期排队","scene":"适合国内短视频创作者、社交媒体运营、创意广告制作"},
    {"name":"HeyGen","icon":"👤","cat":"video","cat_name":"视频生成","url":"https://www.heygen.com","pricing":"免费额度 / Creator $29/月 / Business $89/月","features":"AI数字人视频生成领先，口型同步精准逼真，无需真人出镜，支持多语言数字人，模板丰富易于制作","merit":"数字人口型最逼真,多语言,模板丰富","weakness":"价格较高,免费版有水印","scene":"适合企业培训视频、产品介绍、多语言内容本地化、个人IP打造"},
    {"name":"剪映AI","icon":"✂️","cat":"video","cat_name":"视频生成","url":"https://www.capcut.cn","pricing":"免费 / 部分高级素材付费","features":"字节跳动旗下，国内最流行的视频剪辑工具，AI自动字幕/智能配音/AI调色/数字人/AI视频模板/文本转视频","merit":"完全免费,功能全面,AI字幕好用,模板巨量","weakness":"专业级调色不如达芬奇,高级特效需付费","scene":"适合短视频创作、vlog制作、自媒体日常剪辑、入门级视频制作"},
    {"name":"腾讯智影","icon":"🎞️","cat":"video","cat_name":"视频生成","url":"https://zenvideo.qq.com","pricing":"免费额度 / 会员付费","features":"腾讯出品AI视频创作平台，数字人播报/文本转视频/AI配音/智能字幕，腾讯内容生态支持，素材库丰富","merit":"数字人可选多,腾讯素材多,国产合规","weakness":"视频生成质量中等,创意自由度受限","scene":"适合新闻播报、企业宣传、在线教育视频、内容创作者"},
    {"name":"InVideo","icon":"🎯","cat":"video","cat_name":"视频生成","url":"https://invideo.io","pricing":"免费版（有水印）/ Business $30/月","features":"AI短视频营销利器，海量模板快速出片，文字转视频/文章转视频，社媒视频尺寸自适应，素材库百万+","merit":"模板最多,营销向优化,出片快","weakness":"免费版有水印,自定义程度有限","scene":"适合社交媒体营销、电商产品展示、品牌短视频推广"},
    {"name":"Fliki","icon":"📝","cat":"video","cat_name":"视频生成","url":"https://fliki.ai","pricing":"免费额度 / 订阅$28/月起","features":"文字/博客/RSS一键转视频，AI配音+TTS覆盖75+语言，素材库丰富，适合内容再利用批量生产视频","merit":"文转视频高效,配音语言多,批量生产","weakness":"视频风格偏单一,高级定制受限","scene":"适合博客转视频、内容多渠道分发、批量视频内容生产"},
    {"name":"Descript","icon":"✏️","cat":"video","cat_name":"视频生成","url":"https://www.descript.com","pricing":"免费额度 / Pro $30/月","features":"像编辑Word一样编辑视频/音频，AI转录自动生成字幕，去除语气词/静音一键优化，录屏+编辑一体化","merit":"编辑方式颠覆,AI去语气词好用,录屏编辑一体","weakness":"专业剪辑不如传统软件,中文优化一般","scene":"适合播客制作、教程录制、会议记录编辑、简短视频处理"},
    {"name":"Synthesia","icon":"👨‍💼","cat":"video","cat_name":"视频生成","url":"https://www.synthesia.io","pricing":"Starter $29/月 / Enterprise定制","features":"企业级AI数字人视频平台，140+语言AI数字人，无需拍摄/演员/设备，模板+脚本一键生成，企业培训/营销首选","merit":"企业级方案成熟,多语言覆盖广,省去拍摄成本","weakness":"价格高,数字人情感表达不如真人","scene":"适合企业培训、营销视频、多语言产品介绍、内部沟通视频"},

    # code
    {"name":"GitHub Copilot","icon":"🦾","cat":"code","cat_name":"编程开发","url":"https://github.com/features/copilot","pricing":"Individual $10/月 / Business $19/月 / 学生免费","features":"微软/GitHub出品，深度集成VS Code/JetBrains/Neovim，代码补全精准，根据注释生成函数，Chat模式对话编程，Agent模式自主完成任务","merit":"IDE集成最成熟,补全最精准,生态最完善","weakness":"收费,偶尔生成有bug的代码","scene":"适合所有编程语言的日常开发，是最广泛使用的AI编程助手"},
    {"name":"Claude Code","icon":"⌨️","cat":"code","cat_name":"编程开发","url":"https://claude.ai","pricing":"API付费（按token） / Claude Pro $20/月","features":"Anthropic命令行AI编程工具，终端直接使用，理解整个项目结构，跨文件重构/修bug/写测试，200K上下文一次读整个代码库","merit":"代码理解力最强,跨文件操作,上下文巨大","weakness":"命令行门槛,API付费,需翻墙","scene":"适合后端开发、架构重构、自动化脚本、大型项目代码分析和维护"},
    {"name":"Cursor","icon":"🖱️","cat":"code","cat_name":"编程开发","url":"https://cursor.sh","pricing":"免费额度（2000次补全/月）/ Pro $20/月","features":"基于VS Code深度定制的AI-first编辑器，Tab补全/AI对话修改文件/调试/解释代码，Composer多文件编辑，Agent模式自主编程","merit":"AI编程体验最好,对话式编程,多文件编辑","weakness":"部分插件兼容性问题,更新频繁","scene":"适合追求极致AI编程效率的开发者、全栈工程师、独立开发者"},
    {"name":"Windsurf","icon":"🌊","cat":"code","cat_name":"编程开发","url":"https://codeium.com/windsurf","pricing":"免费 / Teams $15/人/月","features":"Codeium出品免费AI IDE，Cascade流式AI编程体验，多文件上下文理解，自动修复建议，免费额度大方","merit":"免费IDE,AI流式编程,多文件理解","weakness":"新工具生态待完善,补全不如Copilot精准","scene":"适合不想付费的开发者、需要免费AI IDE的学生和个人开发者"},
    {"name":"v0.dev","icon":"🖥️","cat":"code","cat_name":"编程开发","url":"https://v0.dev","pricing":"免费额度 / 订阅$20/月","features":"Vercel推出，自然语言描述生成React/Next.js界面代码，代码可直接复制使用或部署，UI生成质量高，迭代修改方便","merit":"前端UI生成最强,代码可直接用,迭代方便","weakness":"只支持前端React,复杂交互需手调","scene":"适合前端开发、原型快速搭建、Landing Page生成、独立开发者"},
    {"name":"Replit Ghostwriter","icon":"👻","cat":"code","cat_name":"编程开发","url":"https://replit.com","pricing":"免费 / Hacker $25/月","features":"在线IDE内置AI编程助手，浏览器内写代码+部署+协作，AI解释代码/自动补全/生成项目，支持200+语言/框架","merit":"在线IDE+AI一体,无需配置环境,一键部署","weakness":"大型项目受限,性能不如本地","scene":"适合编程学习、快速原型验证、在线协作开发、不用配环境的轻量开发"},
    {"name":"通义灵码","icon":"🐴","cat":"code","cat_name":"编程开发","url":"https://tongyi.aliyun.com/lingma","pricing":"完全免费","features":"阿里出品免费AI编程插件，支持VS Code和JetBrains，中文注释理解突出，Java/Go/Python代码质量好，与阿里云服务整合","merit":"完全免费,中文友好,阿里生态","weakness":"前端代码稍弱,复杂逻辑处理一般","scene":"适合Java/Go后端开发、阿里云用户、学生和国内开发者"},
    {"name":"Bolt.new","icon":"⚡","cat":"code","cat_name":"编程开发","url":"https://bolt.new","pricing":"免费额度 / Pro $20/月","features":"StackBlitz出品，浏览器内AI全栈开发，自然语言描述直接生成全栈Web应用，自动配置环境/依赖/部署，所见即所得","merit":"浏览器内全栈开发,环境零配置,所见即所得","weakness":"复杂项目性能受限,后端语言支持有限","scene":"适合快速原型、MVP验证、Hackathon开发、个人项目快速上线"},
    {"name":"Lovable","icon":"💖","cat":"code","cat_name":"编程开发","url":"https://lovable.dev","pricing":"免费额度 / 订阅制","features":"AI驱动Web应用构建器，自然语言描述生成完整Web应用，支持前端+后端+数据库，一键发布上线","merit":"全栈生成,上手简单,部署一键","weakness":"灵活性不如手写代码,复杂定制受限","scene":"适合无代码/低代码开发者、创业团队MVP、个人Side Project"},
    {"name":"Tabnine","icon":"🔮","cat":"code","cat_name":"编程开发","url":"https://www.tabnine.com","pricing":"免费版 / Pro $12/月 / Enterprise定制","features":"AI代码补全，可本地运行模型保护代码隐私，支持90+语言/20+IDE，企业级安全合规，可根据团队代码库定制训练","merit":"代码隐私保护好,可本地运行,企业安全","weakness":"补全不如GitHub Copilot精准,高级功能企业版","scene":"适合注重代码隐私的企业、金融/医疗等合规行业、私有部署AI编程"},
    {"name":"Sourcegraph Cody","icon":"📈","cat":"code","cat_name":"编程开发","url":"https://sourcegraph.com/cody","pricing":"免费 / Enterprise定制","features":"企业级代码AI助手，理解整个代码仓库上下文，代码搜索+解释+重构+测试生成，Sourcegraph代码搜索平台整合","merit":"企业级代码理解,代码搜索强大,仓库级别上下文","weakness":"偏向大型团队,个人开发者功能溢出","scene":"适合大型代码仓库管理、企业级代码搜索和理解、遗留代码维护"},
    {"name":"Cline","icon":"🤖","cat":"code","cat_name":"编程开发","url":"https://cline.bot","pricing":"免费开源 / API费用自理","features":"VSCode插件AI编程Agent，自主规划-执行-验证循环，可操作文件/运行命令/安装依赖，开源可定制","merit":"开源免费,Agent自主模式,可定制性强","weakness":"消耗API token多,稳定性待提升","scene":"适合探索AI Agent编程的极客、需要自主编程能力的开发者"},

    # office
    {"name":"Notion AI","icon":"📝","cat":"office","cat_name":"办公效率","url":"https://www.notion.so","pricing":"免费版(有限额) / Plus $10/月含AI","features":"笔记+知识库+AI一体化，AI写作/续写/总结/翻译，会议纪要和待办自动生成，数据库视图+AI分析，团队协作无缝","merit":"知识管理+AI完美整合,多功能一体","weakness":"中文优化一般,高级功能Plus才开放","scene":"适合用Notion做知识管理的团队和个人，笔记写作和文档管理场景"},
    {"name":"Gamma","icon":"📊","cat":"office","cat_name":"办公效率","url":"https://gamma.app","pricing":"免费 / Plus $10/月","features":"AI驱动的演示文稿/文档/网页生成，输入主题自动生成精美排版PPT，支持实时协作和数据可视化嵌入，导出PPTX/PDF","merit":"出PPT极快,设计精美,支持协作","weakness":"深度定制需手动调整,付费版才去水印","scene":"适合经常做PPT的职场人、教师、创业者路演、快速Demo展示"},
    {"name":"Grammarly","icon":"✍️","cat":"office","cat_name":"办公效率","url":"https://www.grammarly.com","pricing":"免费 / Premium $12/月","features":"AI英语写作助手标杆，实时语法/拼写/标点检查，根据语境给出风格和语气建议，浏览器插件覆盖所有网页输入框，企业版有品牌语气定制","merit":"英语纠错最强,全平台覆盖,实时反馈","weakness":"中文不支持,免费版功能有限","scene":"适合所有需要用英语写作的人群——学生论文、商务邮件、社媒内容"},
    {"name":"秘塔写作猫","icon":"🐱","cat":"office","cat_name":"办公效率","url":"https://xiezuocat.com","pricing":"免费额度 / 会员付费","features":"中文AI写作助手标杆，文章润色/续写/摘要/改写一站式，中文语法纠错和风格优化，多场景写作模板","merit":"中文写作优化最专业,纠错精准","weakness":"长文生成不如对话式AI,付费额度限制","scene":"适合中文内容创作者、新媒体编辑、需润色文章的写作者"},
    {"name":"ChatPDF","icon":"📄","cat":"office","cat_name":"办公效率","url":"https://www.chatpdf.com","pricing":"免费（每日有限额）/ Plus $5/月","features":"上传PDF直接对话提问，自动提取摘要和要点，支持多文档对比分析，多语言文档理解，学术/合同/报告阅读利器","merit":"PDF问答直观,多文档对比,操作极简","weakness":"免费版文件大小/页数受限,中文PDF理解一般","scene":"适合学生读论文、职场人读合同报告、研究者文献速读"},
    {"name":"Otter.ai","icon":"🎙️","cat":"office","cat_name":"办公效率","url":"https://otter.ai","pricing":"免费 / Pro $16.99/月","features":"AI会议记录工具，实时语音转文字+生成摘要，自动识别说话人，与Zoom/Teams/Meet集成，可搜索回放录音","merit":"会议转录准,自动摘要,集成主流会议工具","weakness":"中文识别不如讯飞,免费版时长有限","scene":"适合英语会议记录、课堂笔记、采访录音整理"},
    {"name":"Beautiful.ai","icon":"💎","cat":"office","cat_name":"办公效率","url":"https://www.beautiful.ai","pricing":"Pro $12/月 / Team $40/月","features":"AI智能PPT设计，自动排版/配色/图表，保持品牌一致性，模板专业设计感强，数据可视化自动生成","merit":"PPT设计自动化,品牌一致性,专业美观","weakness":"需付费,布局自由度不如PPT","scene":"适合市场营销团队、销售提案、投资路演、品牌演示文稿"},
    {"name":"Tome","icon":"📖","cat":"office","cat_name":"办公效率","url":"https://tome.app","pricing":"免费 / Pro $16/月","features":"AI叙事演示工具，一句话主题生成故事性演示文稿，图文排版自动优化，适合创意/教育/商业叙事，嵌入多媒体和交互元素","merit":"叙事感强,视觉效果出众,免费版可用","weakness":"不适合数据密集型报表,个性化调整有限","scene":"适合创意提案、教学设计、品牌故事讲述、个人作品集"},
    {"name":"SlidesAI","icon":"📽️","cat":"office","cat_name":"办公效率","url":"https://www.slidesai.io","pricing":"免费 / Pro $10/月","features":"Google Slides插件AI自动生成PPT，输入文本自动拆分成多页幻灯片，自动配图选模板，支持多语言输出","merit":"Google Slides集成,自动分页,操作简便","weakness":"依赖Google Slides在中国访问不便,功能偏基础","scene":"适合Google Workspace用户、需要快速将文字转PPT的场景"},
    {"name":"Fireflies.ai","icon":"🪰","cat":"office","cat_name":"办公效率","url":"https://fireflies.ai","pricing":"免费 / Pro $18/月","features":"AI会议机器人，自动加入Zoom/Teams/Meet等平台会议，全程录音转录+生成摘要+提取行动项，可搜索历史会议数据库","merit":"自动加入会议省心,行动项提取实用,多平台支持","weakness":"中文识别一般,自动参会需要授权","scene":"适合会议密集的职场人、需要完整会议记录的团队管理者"},
    {"name":"讯飞听见","icon":"👂","cat":"office","cat_name":"办公效率","url":"https://www.iflyrec.com","pricing":"免费额度 / 会员付费","features":"科大讯飞语音转文字王牌产品，中文识别率业界最高，支持实时转写+录音转写，多语种翻译，会议/课程/采访全面覆盖","merit":"中文识别最强,支持方言,多语种翻译","weakness":"高级功能付费,国际会议工具集成不如Otter","scene":"适合国内会议记录、课堂笔记、采访整理、视频字幕制作"},
    {"name":"360AI办公","icon":"🏢","cat":"office","cat_name":"办公效率","url":"https://office.360.cn","pricing":"免费 / 部分高级功能付费","features":"360出品AI办公套件，文档/表格/PPT/PDF全搞定，AI写作/翻译/总结/脑图，国产化适配好无需翻墙","merit":"办公套件全,AI功能多,国产免费","weakness":"单项不如专业工具,品牌调性偏工具型","scene":"适合国内日常办公、中小企业、不需要复杂功能的基础办公"},
    {"name":"DocuAsk","icon":"❓","cat":"office","cat_name":"办公效率","url":"https://www.docuask.com","pricing":"免费额度 / 订阅制","features":"多语言文档对比分析AI，上传多个文档后AI自动对比差异/提取共同点/总结，适合合同/政策/论文对比","merit":"文档对比功能独特,多语言支持","weakness":"小众产品,功能较窄","scene":"适合法律合同对比、政策文件分析、学术文献比较研究"},
    {"name":"Humata","icon":"📑","cat":"office","cat_name":"办公效率","url":"https://www.humata.ai","pricing":"免费 / Pro $9.99/月","features":"PDFAI问答助手，像ChatGPT一样和你的文档对话，自动总结长文要点，支持跨文档提问，科研/技术文档阅读加速","merit":"PDF问答智能,跨文档搜索,科研友好","weakness":"免费版上传有限,非英语文档理解待提升","scene":"适合科研人员文献速读、技术人员文档查询、法务合同审核"},

    # audio
    {"name":"Suno","icon":"🎵","cat":"audio","cat_name":"音频音乐","url":"https://suno.com","pricing":"免费额度（每日）/ Pro $10/月","features":"最火的AI音乐生成工具，输入歌词+风格提示即可生成完整歌曲，V4版本音质大幅提升接近广播级，多种音乐风格支持","merit":"音乐生成质量最高,操作简单,风格广泛","weakness":"付费,版权归属模糊,偶有生成失败","scene":"适合音乐爱好者创作、短视频配乐、独立音乐人灵感获取、个人娱乐"},
    {"name":"ElevenLabs","icon":"🗣️","cat":"audio","cat_name":"音频音乐","url":"https://elevenlabs.io","pricing":"免费（1万字符/月）/ Starter $5/月 / Pro $22/月","features":"AI语音合成天花板，语音极其自然接近真人，支持29+语言和声音克隆，情感表达丰富细腻，API可用","merit":"语音最自然,多语言,声音克隆逼真","weakness":"付费,免费版字数限制","scene":"适合视频配音、有声书制作、播客录制、多语言内容本地化"},
    {"name":"Udio","icon":"🎹","cat":"audio","cat_name":"音频音乐","url":"https://www.udio.com","pricing":"免费额度 / 订阅制","features":"前Google DeepMind研究员创立，音质优秀媲美Suno，人声+伴奏分离生成，32秒片段的音乐性特别强，社区活跃创意多","merit":"音质优秀,人声表现力好,社区活跃","weakness":"版权政策待明确,免费额度有限","scene":"适合音乐制作人、创意工作者、对音质有追求的音乐爱好者"},
    {"name":"Murf.ai","icon":"🎤","cat":"audio","cat_name":"音频音乐","url":"https://murf.ai","pricing":"免费 / Pro $29/月","features":"专业AI配音工具，120+音色可选，语速/音调/强调可精确调节，支持视频配音同步，适合商业配音场景","merit":"音色丰富,配音参数可控,商业用途","weakness":"价格偏高,免费版功能有限","scene":"适合商业视频配音、广告旁白、企业培训课件配音、有声内容制作"},
    {"name":"Audiobox","icon":"📻","cat":"audio","cat_name":"音频音乐","url":"https://audiobox.metademolab.com","pricing":"免费（研究预览版）","features":"Meta出品AI音效和声音生成，文字描述生成定制音效，声音风格迁移和定制，学术研究级别的声音理解","merit":"免费,Meta研究院出品,音效生成独特","weakness":"研究阶段功能不稳定,商业化不足","scene":"适合音效设计师、游戏音效创意、AI声音研究探索"},
    {"name":"剪映配音","icon":"🎬","cat":"audio","cat_name":"音频音乐","url":"https://www.capcut.cn","pricing":"免费","features":"剪映内置AI配音功能，多音色可选覆盖男女老少，语速语调可调，自动对齐视频字幕，和剪辑流程无缝衔接","merit":"免费,与剪辑流程一体,中文音色多","weakness":"音色自然度不如ElevenLabs,高级情感控制弱","scene":"适合短视频配音、vlog旁白、自媒体内容制作、入门级配音需求"},
    {"name":"Soundraw","icon":"🎼","cat":"audio","cat_name":"音频音乐","url":"https://soundraw.io","pricing":"免费额度 / Pro $19.99/月","features":"AI无版权音乐生成，商用友好，按情绪/节奏/风格/时长定制背景音乐，生成的音乐可放心用于商业项目","merit":"无版权,商用安全,情绪定制","weakness":"免费版导出受限,风格偏BGM","scene":"适合视频背景音乐、播客配乐、商业项目避免版权纠纷"},
    {"name":"Beatoven","icon":"🥁","cat":"audio","cat_name":"音频音乐","url":"https://www.beatoven.ai","pricing":"免费额度 / 订阅制","features":"AI情绪驱动的背景音乐生成，输入情绪/场景/风格提示出BGM，视频配音同步，多种氛围/风格可选","merit":"情绪匹配好,适合BGM,视频同步","weakness":"风格偏氛围类,人声歌曲不支持","scene":"适合视频配乐、游戏背景音乐、冥想/睡眠音乐、播客配乐"},
    {"name":"Adobe Podcast","icon":"🎧","cat":"audio","cat_name":"音频音乐","url":"https://podcast.adobe.com","pricing":"免费","features":"Adobe出品AI音频后期工具，一键降噪去混响效果惊艳，远程录音音质增强，AI麦克风诊断，免费使用","merit":"AI降噪效果惊艳,完全免费,Adobe品质","weakness":"功能偏后期处理,非音乐创作工具","scene":"适合播客录制后期、远程采访音质优化、视频配音降噪"},
    {"name":"网易天音","icon":"🎶","cat":"audio","cat_name":"音频音乐","url":"https://tianyin.163.com","pricing":"免费额度 / 会员付费","features":"网易出品AI音乐创作平台，中文词曲理解优秀，一键生成歌词/编曲/混音，华语音乐风格丰富，编曲专业度好","merit":"中文词曲优化,编曲专业,国产最成熟","weakness":"风格偏流行,高级定制受限","scene":"适合华语音乐创作、demo制作、短视频配乐、音乐爱好者"},

    # agent
    {"name":"AutoGPT","icon":"🤖","cat":"agent","cat_name":"AI Agent","url":"https://github.com/Significant-Gravitas/AutoGPT","pricing":"开源免费 / API费用自理","features":"开源AI Agent鼻祖，设定目标后自动分解任务/搜索信息/执行操作/自我纠错，可接入多种LLM后端，代表了AI自主化的方向","merit":"自主性强,开源,愿景宏大","weakness":"稳定性不够,消耗token多,实用价值待提升","scene":"适合AI研究者、极客探索自动化、Agent技术学习和实验"},
    {"name":"MetaGPT","icon":"🏢","cat":"agent","cat_name":"AI Agent","url":"https://github.com/geekan/MetaGPT","pricing":"开源免费 / API费用自理","features":"模拟软件公司的多Agent框架，自动完成需求分析/架构设计/编码/测试全流程，多角色协作（PM/架构师/工程师/测试）","merit":"软件工程全流程,学术背景深厚,开源","weakness":"实际产出需人工把关,运行成本高","scene":"适合软件工程研究、自动化代码生成探索、教育演示多Agent协作"},
    {"name":"CrewAI","icon":"👥","cat":"agent","cat_name":"AI Agent","url":"https://www.crewai.com","pricing":"开源 / Enterprise定制","features":"多AI Agent编排框架，定义不同角色Agent组成协作团队，任务自动分配和调度，模拟真实公司内部协作流程","merit":"多Agent协作设计好,角色分工清晰,社区增长快","weakness":"文档更新慢,实际落地需开发","scene":"适合企业流程自动化、研发团队AI实验、多Agent系统研究和应用"},
    {"name":"Coze","icon":"🧩","cat":"agent","cat_name":"AI Agent","url":"https://www.coze.com","pricing":"免费 / 企业版收费","features":"字节跳动国际版AI Bot搭建平台，零代码创建AI智能体，丰富插件生态（搜索/图片/数据），可接入Discord/Telegram等多渠道","merit":"零代码,插件多,多平台分发,免费","weakness":"复杂逻辑需学习,企业功能收费","scene":"适合想搭建AI客服、社群机器人、个人AI助手的非开发者"},
    {"name":"Dify","icon":"🔧","cat":"agent","cat_name":"AI Agent","url":"https://dify.ai","pricing":"开源免费 / Cloud免费额度 / Enterprise定制","features":"最流行的开源LLM应用开发平台，可视化搭建RAG/Agent/工作流，支持多种LLM切换，可私有部署数据安全","merit":"开源最热,可视化,私有部署,多模型","weakness":"高级工作流需学习,部署需要服务器","scene":"适合企业AI应用搭建、开发者构建AI工作流、数据安全的私有AI场景"},
    {"name":"扣子","icon":"🪢","cat":"agent","cat_name":"AI Agent","url":"https://www.coze.cn","pricing":"免费","features":"抖音旗下AI智能体平台（Coze中国版），零代码搭建Bot，插件生态丰富，接入飞书/微信/抖音等国内渠道","merit":"免费,国内渠道多,零代码,生态丰富","weakness":"依赖字节生态,国际版和国内版功能差异","scene":"适合国内企业搭建AI客服/营销Bot、个人创作者搭建粉丝互动机器人"},
    {"name":"AgentGPT","icon":"🎯","cat":"agent","cat_name":"AI Agent","url":"https://agentgpt.reworkd.ai","pricing":"免费额度 / 订阅制","features":"浏览器端自主AI Agent，设定目标+名字后Agent自动分解任务执行，可视化任务进度，无需编程即可体验Agent概念","merit":"浏览器直接体验Agent,可视化,免费","weakness":"实际完成率不高,高级任务表现一般","scene":"适合AI Agent概念体验、简单自动化任务、教学演示"},
    {"name":"BabyAGI","icon":"👶","cat":"agent","cat_name":"AI Agent","url":"https://github.com/yoheinakajima/babyagi","pricing":"开源免费 / API费用自理","features":"极简任务驱动AI Agent框架，代码仅100+行但概念清晰，任务创建-执行-优先级排序循环，Agent入门经典","merit":"极简开源,概念清晰,学习Agent入门","weakness":"功能基础,生产环境不适用","scene":"适合AI Agent学习和研究、Agent概念验证、教学演示"},
    {"name":"文心智能体","icon":"🧠","cat":"agent","cat_name":"AI Agent","url":"https://agents.baidu.com","pricing":"免费","features":"百度AI智能体平台，快速搭建专属Bot，百度搜索/文心大模型赋能，知识库问答/工具调用/多轮对话支持","merit":"免费,百度生态整合,中文优秀","weakness":"依赖百度生态,开放性不如Dify","scene":"适合国内用户搭建专属AI助手、企业客服Bot、百度搜索整合场景"},

    # search
    {"name":"You.com","icon":"🔍","cat":"search","cat_name":"AI搜索引擎","url":"https://you.com","pricing":"免费 / Pro $14.99/月","features":"AI搜索引擎先驱，隐私优先（不追踪用户），多模式可选（智能/研究/创意等），整合Chat/图片/代码等多类型结果","merit":"隐私保护好,多模式切换,答案直观","weakness":"知名度不如Perplexity,中文支持一般","scene":"适合注重隐私的用户、需要多种搜索模式的场景、海外AI搜索替代品"},
    {"name":"Phind","icon":"💻","cat":"search","cat_name":"AI搜索引擎","url":"https://www.phind.com","pricing":"免费额度 / Phind Plus订阅","features":"开发者专用AI搜索引擎，搜索+回答融合代码示例，技术问题回答质量高，支持多模型后端切换，编程社区口碑好","merit":"技术搜索最强,代码示例丰富,编程社区认可","weakness":"非技术搜索不如通用搜索引擎,免费有限额","scene":"适合程序员技术搜索、Debug查资料、学习新技术栈"},
    {"name":"Microsoft Copilot","icon":"🪟","cat":"search","cat_name":"AI搜索引擎","url":"https://copilot.microsoft.com","pricing":"免费 / Copilot Pro $20/月","features":"微软AI搜索，基于GPT-4 Turbo+必应实时搜索，DALL·E 3图像生成，三种对话风格切换（创意/平衡/精准），Edge侧边栏集成","merit":"免费GPT-4,必应实时搜索,多模式","weakness":"国内访问不便,回答长度有限","scene":"适合国际信息搜索、需要图文并茂答案的用户、Windows/Edge用户"},
    {"name":"Consensus","icon":"📚","cat":"search","cat_name":"AI搜索引擎","url":"https://consensus.app","pricing":"免费 / Premium $11.99/月","features":"AI学术搜索引擎，直接搜索2亿+篇论文得出结论，带精确引用，研究共识度指标，适合快速了解学术领域","merit":"学术搜索专业,直接给结论,引用精确","weakness":"仅限学术场景,覆盖面不如通用搜索","scene":"适合研究人员、学生写论文、快速了解某个领域的学术共识"},
    {"name":"Devv","icon":"🤖","cat":"search","cat_name":"AI搜索引擎","url":"https://devv.ai","pricing":"免费","features":"中文开发者AI搜索引擎，代码问答+搜索+翻译一站式，中文技术问题理解好，国内开发者社区口碑产品","merit":"中文技术搜索好,免费,开发者社区认可","weakness":"品牌较新,非技术搜索覆盖少","scene":"适合国内程序员技术搜索、中文开发问题解答、新技术学习"},
    {"name":"秘塔AI搜索","icon":"🔎","cat":"search","cat_name":"AI搜索引擎","url":"https://metaso.cn","pricing":"免费","features":"国产AI搜索引擎标杆，无广告直达答案，自动总结网页内容+生成思维导图+提取关键信息，学术模式搜论文，文库模式搜专业文档","merit":"免费,无广告,中文搜索优,多模式","weakness":"英文覆盖不如Perplexity,偶尔幻觉","scene":"适合国内用户日常搜索、论文调研、专业知识检索"},

    # design
    {"name":"Figma AI","icon":"🎨","cat":"design","cat_name":"AI设计工具","url":"https://www.figma.com/ai","pricing":"免费版(有限功能) / Pro $12/月 / Enterprise $45/月","features":"Figma内置AI设计助手，设计草图/截图一键转高保真界面，自动生成设计内容/文案，智能布局和组件变体，团队协作+AI提效","merit":"UI设计行业标准,协作最强,AI辅助自然","weakness":"高级AI功能还在逐步推出,学习有门槛","scene":"适合UI/UX设计师、产品团队、设计系统维护、界面快速迭代"},
    {"name":"Uizard","icon":"✨","cat":"design","cat_name":"AI设计工具","url":"https://uizard.io","pricing":"免费 / Pro $12/月","features":"手绘草图/截图秒变UI设计稿，支持一键切换设计风格/主题，拖拽式编辑器+AI生成组件，产品经理也能做原型","merit":"草图转UI惊艳,非设计师可用,快速原型","weakness":"高保真不如Figma,复杂交互受限","scene":"适合产品经理快速原型、创业团队MVP设计、快速验证产品概念"},
    {"name":"Galileo AI","icon":"🔭","cat":"design","cat_name":"AI设计工具","url":"https://www.usegalileo.ai","pricing":"等待列表 / 即将公布定价","features":"自然语言描述直接生成完整UI界面设计，AI理解设计意图自动匹配组件和布局，设计稿可直接导出到Figma","merit":"文字转UI设计前沿,节约设计时间","weakness":"尚未完全开放,精细设计需人工调整","scene":"适合快速UI创意探索、设计灵感获取、初级设计师辅助"},
    {"name":"Looka","icon":"🏷️","cat":"design","cat_name":"AI设计工具","url":"https://looka.com","pricing":"Basic $20一次性 / Premium $65一次性","features":"AI Logo设计+品牌VI一键生成，输入品牌名+行业自动生成数百个Logo方案，配套名片/信纸/社媒素材等全套VI","merit":"Logo设计快,品牌VI一站式,一次性收费","weakness":"生成Logo有模板感,高端定制受限","scene":"适合初创企业Logo设计、个人品牌VI、预算有限需要快速出品牌的场景"},
    {"name":"Khroma","icon":"🎨","cat":"design","cat_name":"AI设计工具","url":"https://www.khroma.co","pricing":"免费","features":"AI配色工具，根据个人偏好训练生成无限配色方案，可查看配色在实际UI中的效果，导出调色板到设计工具","merit":"免费,个性化配色训练,预览真实","weakness":"功能单一仅配色,依赖个人训练","scene":"适合设计师配色灵感、品牌主色调探索、UI设计和网页设计的配色方案"},
    {"name":"Autodraw","icon":"✏️","cat":"design","cat_name":"AI设计工具","url":"https://www.autodraw.com","pricing":"免费","features":"Google出品趣味AI绘画工具，随手潦草涂鸦AI自动识别并替换为精美图标，简单好玩老少皆宜，下载PNG免费使用","merit":"完全免费,有趣易用,Google出品","weakness":"功能极简,只适合图标/简笔画","scene":"适合快速画简笔画图标、非设计师制作简单插图、教育和趣味场景"},

    # marketing
    {"name":"Jasper","icon":"✍️","cat":"marketing","cat_name":"AI营销写作","url":"https://www.jasper.ai","pricing":"Creator $49/月 / Pro $69/月","features":"海外AI营销文案标杆，品牌声音定制（Brand Voice），覆盖广告/落地页/邮件/社媒/Blog/SEO全场景，团队协作+内容日历","merit":"营销场景最专业,品牌声音定制,内容全覆盖","weakness":"价格较高,中文支持一般","scene":"适合市场营销团队、广告公司、品牌内容运营、需要规模化产出营销内容的企业"},
    {"name":"Copy.ai","icon":"📢","cat":"marketing","cat_name":"AI营销写作","url":"https://www.copy.ai","pricing":"免费版 / Pro $49/月","features":"轻量级AI营销文案生成，社媒帖子/产品描述/广告语等短文案尤其出色，操作极简单，Workflow自动化批量生成","merit":"短文案出色,操作简单,Workflow自动化","weakness":"长文案能力弱,品牌定制性不足","scene":"适合社交媒体运营、电商卖家、需要快速批量产出短文案的小团队"},
    {"name":"Writesonic","icon":"📝","cat":"marketing","cat_name":"AI营销写作","url":"https://writesonic.com","pricing":"免费额度 / 订阅从$20/月起","features":"全能型AI营销内容平台，博客/广告/SEO/社媒/电商全覆盖，AI聊天+图像生成一体化，事实核查功能","merit":"功能全面,SEO优化,图文一体","weakness":"中文内容质量波动,高级功能付费","scene":"适合内容营销全流程、SEO优化、多平台内容分发的中小团队"},
    {"name":"火山写作","icon":"🌋","cat":"marketing","cat_name":"AI营销写作","url":"https://www.huoshanai.com","pricing":"免费额度 / 会员付费","features":"字节跳动旗下AI写作工具，热点追踪快（头条/抖音数据），中文营销文案优化强，多种内容风格一键切换","merit":"热点追踪强,短文案出色,免费额度大","weakness":"长文深度不够,偏向短视频文案风格","scene":"适合抖音/头条创作者、热点营销、短视频配套文案创作"},
    {"name":"易撰","icon":"📰","cat":"marketing","cat_name":"AI营销写作","url":"https://www.yizhuan5.com","pricing":"免费额度 / VIP付费","features":"自媒体创作工具，爆文分析追踪+AI写作，各平台（公众号/头条/百家号）内容适配，数据分析辅助选题","merit":"自媒体生态整合,爆文分析,多平台适配","weakness":"内容同质化风险,依赖平台数据","scene":"适合国内自媒体运营者、需要批量产出平台适配内容的创作者"},
    {"name":"爱撰写","icon":"🛒","cat":"marketing","cat_name":"AI营销写作","url":"https://www.aizhuanxie.com","pricing":"免费额度 / 会员付费","features":"电商AI文案专家，淘宝/京东/拼多多等平台商品标题和详情页优化，批量生成SKU文案，提升搜索排名转化率","merit":"电商文案专业,多平台适配,批量生成","weakness":"仅限电商场景,风格偏商业","scene":"适合电商卖家、店铺运营、需要大量优化商品文案和详情页的商家"},

    # edu
    {"name":"Duolingo Max","icon":"🦉","cat":"edu","cat_name":"AI学习教育","url":"https://www.duolingo.com","pricing":"免费版 / Super $12.99/月 / Max $29.99/月","features":"多邻国AI高级版，GPT-4驱动角色扮演对话练习和答案解释，模拟真实对话场景练习外语，解释你的错误原因","merit":"对话练习真实,错误解释到位,游戏化趣味强","weakness":"Max版贵,主要面向英语学习者","scene":"适合外语学习者、想提升口语对话能力的成人、需要个性化反馈的语言学习"},
    {"name":"Khanmigo","icon":"🎓","cat":"edu","cat_name":"AI学习教育","url":"https://www.khanacademy.org/khan-labs","pricing":"$44/年（教育折扣）/ 教师免费","features":"可汗学院AI辅导系统，苏格拉底式一对一智能教学，不直接给答案而是引导学生思考，数学/科学/人文多学科覆盖","merit":"启发式教学不灌输,多学科,教师免费","weakness":"价格对个人偏高,需可汗学院账号","scene":"适合K12学生课外辅导、家长辅助教学、教师课堂辅助工具"},
    {"name":"Quizlet AI","icon":"📝","cat":"edu","cat_name":"AI学习教育","url":"https://quizlet.com","pricing":"免费 / Quizlet Plus $7.99/月","features":"老牌学习工具AI升级版，Q-Chat功能像老师一样苏格拉底式提问帮助理解，AI自动生成闪卡/测试题，间隔重复记忆算法","merit":"记忆效率高,AI互动提问,学生群体大","weakness":"中文内容少,深度讲解不如真人","scene":"适合语言单词记忆、概念复习、考前冲刺背诵、自主复习的学生"},
    {"name":"作业帮","icon":"📖","cat":"edu","cat_name":"AI学习教育","url":"https://www.zybang.com","pricing":"免费 / VIP功能付费","features":"国产K12学习平台，拍照搜题/AI讲解/知识点诊断/个性化学习路径，题库量行业最大，全科覆盖从小学到高中","merit":"题库量最大,全科覆盖,拍照搜题好用","weakness":"VIP功能需付费,依赖手机使用","scene":"适合K12学生日常作业辅导、考前复习、家长检查作业"},
    {"name":"学而思AI","icon":"🏫","cat":"edu","cat_name":"AI学习教育","url":"https://www.xueersi.com","pricing":"免费体验 / 课程付费","features":"学而思AI教育平台，自适应学习系统根据学生水平动态调整难度，直播+AI双师模式，主科辅导深入","merit":"自适应学习,双师模式,教研体系成熟","weakness":"课程体系付费,AI功能辅助为主","scene":"适合希望系统提分的K12学生、需要专业教研体系的家庭"},

    # data
    {"name":"Julius AI","icon":"📊","cat":"data","cat_name":"AI数据分析","url":"https://julius.ai","pricing":"免费额度 / 订阅从$20/月起","features":"对话式数据分析工具，上传CSV/Excel/Google Sheet后自然语言提问，自动生成统计分析和可视化图表，支持多种图表类型和统计检验","merit":"对话式分析自然,图表美观,统计分析专业","weakness":"免费版数据量有限,高级分析需付费","scene":"适合数据分析师、研究人员、学生做统计作业、快速数据探索"},
    {"name":"Obviously AI","icon":"🤖","cat":"data","cat_name":"AI数据分析","url":"https://www.obviously.ai","pricing":"免费试用 / 订阅从$80/月起","features":"无代码AI预测建模平台，拖拽上传数据自动构建ML模型，自动选择最佳算法+调参，一键部署预测API","merit":"无代码ML,自动选算法,预测建模快","weakness":"价格较高,高级定制受限","scene":"适合无数据科学背景的业务人员、中小企业快速预测建模"},
    {"name":"Rows","icon":"📈","cat":"data","cat_name":"AI数据分析","url":"https://rows.com","pricing":"免费 / Pro $19/月","features":"AI增强在线表格，Excel+ChatGPT合体体验，自然语言描述生成数据分析/图表/公式，内置丰富数据集成（API/数据库等）","merit":"表格+AI融合,数据集成多,免费可用","weakness":"复杂分析不如专业BI,中国市场知名度低","scene":"适合日常数据处理、快速数据分析、替代Excel做智能报表"},
    {"name":"WPS AI","icon":"📋","cat":"data","cat_name":"AI数据分析","url":"https://ai.wps.cn","pricing":"免费额度 / WPS会员含更多AI功能","features":"金山WPS内置AI，表格/文档/PPT/PDF全AI支持，国产办公软件用户基数最大，表格AI分析+文档AI写作+PPT AI生成","merit":"国产覆盖最广,办公套件AI,免费额度","weakness":"AI能力不如专业工具,会员功能限制","scene":"适合国内WPS用户、日常办公数据处理、不需要专业BI的普通用户"},
]

# ---- Category names mapping ----
cat_names = {
    "chat":"对话聊天","image":"图像创作","video":"视频生成","code":"编程开发",
    "office":"办公效率","audio":"音频音乐","agent":"AI Agent","search":"AI搜索引擎",
    "design":"AI设计工具","marketing":"AI营销写作","edu":"AI学习教育","data":"AI数据分析"
}

# ---- Content templates ----
intros = [
    "{name}是{desc_short}。作为{cat_name}领域的佼佼者，{name}凭借其出色的性能和独特的定位，赢得了大量用户的青睐。本文将从功能介绍、优缺点分析、使用场景、定价策略等多个维度，为你全面解析{name}，帮你判断它是否适合你的需求。",
    "在{cat_name}领域，{name}是一个不容忽视的存在。{desc_short}。无论你是新手还是老手，这篇深度评测都能帮你了解{name}的真实实力，避免盲选踩坑。",
    "你可能已经在各种AI工具榜单上看到过{name}的名字。{desc_short}。但榜单只是一个名字，真正的实力需要深入体验才能判断——这篇实测报告给你答案。",
]

usecase_intros = [
    "什么人最适合用{name}？如果你的工作或创作涉及{scene}，那{name}就是为你量身打造的。以下是一些典型的使用场景：",
    "{name}并非适合所有人，但如果你是{scene}的用户，它会让你爱不释手。来看看它在实际场景中的表现：",
    "根据大量用户反馈和实际体验，{name}在{scene}等场景下表现最为亮眼。以下是几个典型的使用案例：",
]

pros_cons_templates = [
    "综合来看，{name}毫无疑问是{cat_name}赛道的实力派选手。{merit}是它的核心竞争力。当然，{weakness}也是目前客观存在的短板。但瑕不掩瑜，在大多数使用场景下，{name}的表现都足够令人满意。",
    "经过一段时间的深度使用，{name}给我最大的感受是：{merit}。不过{weakness}这点确实需要在选择前考虑清楚。总体而言，如果你的需求和它的定位匹配，{name}会是一个高性价比的选择。",
    "{name}最大的价值在于{merit}。当然它也不是万能的——{weakness}。但如果你正好需要它在强项上的能力，那么这些小缺点都是可以接受的。",
]

# ---- Build pages ----
count = 0
for t in tools:
    slug = t["name"].lower().replace(" ","-").replace(".","").replace("·","").replace(" ","-")
    slug = slug.replace("(","").replace(")","").replace("'","")
    fname = f"{slug}.html"
    fpath = os.path.join(TOOLS_DIR, fname)

    cat_name = cat_names.get(t["cat"], t["cat_name"])

    # Build content
    intro = random.choice(intros).format(
        name=t["name"], cat_name=cat_name,
        desc_short=f'{t["name"]}是一款{t["features"][:50]}'
    )

    usecase_intro = random.choice(usecase_intros).format(
        name=t["name"], scene=t.get("scene",""), cat_name=cat_name
    )
    pos_neg = random.choice(pros_cons_templates).format(
        name=t["name"], merit=t.get("merit",""), weakness=t.get("weakness",""), cat_name=cat_name
    )

    # Pick 3 similar tools from same category
    same_cat = [x for x in tools if x["cat"] == t["cat"] and x["name"] != t["name"]]
    similar = random.sample(same_cat, min(3, len(same_cat)))

    similar_html = ""
    for s in similar:
        s_slug = s["name"].lower().replace(" ","-").replace(".","").replace("·","").replace("(","").replace(")","")
        similar_html += f'<a href="{s_slug}.html" class="similar-link">{s["icon"]} {s["name"]}</a>\n'

    feat_items = [f.strip() for f in t.get("features","").split("，")[:5]]
    feat_html = ""
    for f in feat_items:
        feat_html += f"<li>{f}</li>\n"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{t['name']} - {t.get('desc','')} | 功能介绍、优缺点分析、定价、使用场景全评测">
<meta name="keywords" content="{t['name']},{cat_name},AI工具,{t['name']}评测,{t['name']}教程">
<meta name="author" content="AI工具箱">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{BASE_URL}/tools/{urllib.parse.quote(fname)}">
<meta property="og:title" content="{t['name']} - {cat_name} | AI工具箱">
<meta property="og:description" content="{t['name']}深度评测：{t.get('desc','')}">
<meta property="og:type" content="article">
<meta property="og:url" content="{BASE_URL}/tools/{urllib.parse.quote(fname)}">
<meta property="og:site_name" content="AI工具箱">
<meta name="twitter:card" content="summary">
<meta name="google-adsense-account" content="ca-pub-9833675612669955">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9833675612669955" crossorigin="anonymous"></script>
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-50DB4RCNL3"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-50DB4RCNL3');</script>
<title>{t['name']} - {cat_name}工具评测 | AI工具箱</title>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "{t['name']}",
  "description": "{t.get('desc','')}",
  "applicationCategory": "AIApplication",
  "operatingSystem": "Web",
  "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "CNY"}},
  "url": "{BASE_URL}/tools/{urllib.parse.quote(fname)}"
}}
</script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0d1117;color:#c9d1d9;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.6;padding:20px;max-width:800px;margin:0 auto}}
h1{{font-size:22px;color:#fff;margin-bottom:6px;line-height:1.4}}
h2{{font-size:18px;color:#d4a574;margin:30px 0 16px;border-left:3px solid #d4a574;padding-left:12px}}
h3{{font-size:16px;margin-bottom:6px}}
p{{margin-bottom:14px;color:#8b949e;font-size:15px}}
li{{color:#8b949e;font-size:14px;margin-bottom:6px;margin-left:20px}}
a{{color:#58a6ff;text-decoration:none}}
.nav{{margin-bottom:20px;font-size:13px}}
.nav a{{color:#8b949e}}
.header{{text-align:center;padding:20px 0;border-bottom:1px solid #30363d;margin-bottom:30px}}
.header .icon{{font-size:60px;display:block;margin-bottom:12px}}
.header .cat{{display:inline-block;padding:2px 10px;border-radius:12px;font-size:11px;background:rgba(88,166,255,0.1);color:#58a6ff;margin-top:8px}}
.info-box{{background:#161b22;border:1px solid #30363d;border-radius:12px;padding:20px;margin:20px 0;display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.info-box .label{{font-size:12px;color:#8b949e}}
.info-box .value{{font-size:14px;color:#fff}}
.btn-visit{{display:inline-block;padding:12px 32px;border-radius:24px;background:linear-gradient(135deg,#d4a574,#e6b980);color:#000;text-decoration:none;font-weight:700;font-size:15px;text-align:center;margin:12px 0}}
.btn-visit:hover{{opacity:0.9}}
.ad-unit{{margin:24px 0;padding:8px 0;border-top:1px solid #30363d;border-bottom:1px solid #30363d}}
.similar-box{{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:16px;margin:20px 0}}
.similar-link{{display:inline-block;padding:6px 14px;margin:4px;border-radius:20px;background:#1a2332;color:#58a6ff;text-decoration:none;font-size:13px;transition:.15s;border:1px solid #30363d}}
.similar-link:hover{{border-color:#58a6ff;color:#fff}}
footer{{text-align:center;padding:30px 0;margin-top:40px;border-top:1px solid #30363d;font-size:13px;color:#8b949e}}
footer a{{color:#8b949e}}
@media(max-width:600px){{body{{padding:12px}}h1{{font-size:18px}}.info-box{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="nav"><a href="/">← 返回AI工具箱首页</a> · <a href="/articles/">评测文章</a> · <a href="/tools/">工具详情</a></div>
<article>
<div class="header">
  <span class="icon">{t['icon']}</span>
  <h1>{t['name']}</h1>
  <p>{t.get('desc','')}</p>
  <span class="cat">{cat_name}</span>
</div>

<h2>工具简介</h2>
<p>{intro}</p>

<div class="info-box">
  <div><div class="label">产品类型</div><div class="value">{cat_name}</div></div>
  <div><div class="label">价格</div><div class="value">{t.get('pricing','详见官网')}</div></div>
  <div><div class="label">官方网站</div><div class="value"><a href="{t['url']}" target="_blank" rel="noopener nofollow">访问官网 →</a></div></div>
  <div><div class="label">适合人群</div><div class="value">{t.get('scene','')[:40]}...</div></div>
</div>

<a href="{t['url']}" class="btn-visit" target="_blank" rel="noopener nofollow" style="display:block;width:fit-content;margin:0 auto">🔗 访问官网</a>

<h2>核心功能</h2>
<ul>
{feat_html}
</ul>

<h2>实际使用场景</h2>
<p>{usecase_intro}</p>
<p>{t.get('scene','')}</p>

<div class="ad-unit">
<ins class="adsbygoogle"
     style="display:block;text-align:center;margin:24px 0"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="ca-pub-9833675612669955"
     data-ad-slot="REPLACE-WITH-SLOT-ID-1"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
</div>

<h2>综合评价</h2>
<p><span style="color:#4caf50">✓ 优势：</span>{t.get('merit','')}</p>
<p><span style="color:#e67e22">△ 不足：</span>{t.get('weakness','')}</p>
<p>{pos_neg}</p>

<div class="ad-unit">
<ins class="adsbygoogle"
     style="display:block;text-align:center;margin:24px 0"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="ca-pub-9833675612669955"
     data-ad-slot="REPLACE-WITH-SLOT-ID-2"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
</div>

<h2>同类工具推荐</h2>
<div class="similar-box">
{similar_html}
</div>

</article>
<footer>
  <p>AI工具箱 © 2026 · <a href="/">返回首页</a> · <a href="/privacy.html">隐私政策</a> · <a href="/articles/">文章列表</a></p>
</footer>
</body>
</html>"""

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html)
    count += 1

# Generate tools index page
tool_links = ""
for cat, cname in cat_names.items():
    cat_tools = [t for t in tools if t["cat"] == cat]
    tool_links += f'<div class="cat-section"><h2>{cname}</h2>\n'
    for t in cat_tools:
        slug = t["name"].lower().replace(" ","-").replace(".","").replace("·","").replace("(","").replace(")","")
        tool_links += f'  <a class="tool-link" href="{slug}.html">{t["icon"]} {t["name"]}</a>\n'
    tool_links += '</div>\n'

ld_json = """{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "AI工具详情列表",
  "description": "收录110款AI工具详细信息",
  "url": "https://aitools-khaki.vercel.app/tools/"
}"

idx_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="AI工具箱 - {len(tools)}款AI工具详细评测，涵盖{len(cat_names)}个分类，每款工具都有功能介绍、优缺点、使用场景和定价信息">
<meta name="keywords" content="AI工具评测,AI工具详情,AI工具介绍">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{BASE_URL}/tools/">
<meta property="og:title" content="AI工具详情 - {len(tools)}款工具深度评测 | AI工具箱">
<meta property="og:description" content="收录{len(tools)}款AI工具的详细介绍，涵盖{len(cat_names)}个分类">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE_URL}/tools/">
<meta property="og:site_name" content="AI工具箱">
<title>AI工具详情 · 共{len(tools)}款 - AI工具箱</title>
<script type="application/ld+json">
{ld_json}
</script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0d1117;color:#c9d1d9;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;padding:20px;max-width:900px;margin:0 auto}}
h1{{font-size:22px;color:#fff;text-align:center;margin:20px 0;padding-bottom:16px;border-bottom:1px solid #30363d}}
.cat-section{{margin:30px 0}}
.cat-section h2{{font-size:18px;color:#d4a574;margin-bottom:12px}}
.tool-link{{display:inline-block;padding:8px 14px;margin:3px;background:#161b22;border-radius:20px;color:#c9d1d9;text-decoration:none;font-size:13px;transition:.15s;border:1px solid #30363d}}
.tool-link:hover{{background:#1a2332;border-color:#58a6ff;color:#fff}}
.back{{text-align:center;margin-top:30px}}
.back a{{color:#58a6ff}}
</style>
</head>
<body>
<h1>AI工具详情 · 共{len(tools)}款</h1>
{tool_links}
<div class="back"><a href="/">← 返回AI工具箱首页</a></div>
</body>
</html>"""

with open(os.path.join(TOOLS_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(idx_html)

print(f"Generated {count} tool detail pages + tools index page in: {TOOLS_DIR}")
