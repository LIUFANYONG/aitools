"""
Generate 100 SEO-optimized AI tool articles.
Each ~800 words, structured: pain point → intro → compare → use case → recommend.
Run: python generate_articles.py
"""
import os, random, time

OUT = os.path.join(os.path.dirname(__file__), "articles")
os.makedirs(OUT, exist_ok=True)

# ── SEO keyword pools ──
title_templates = [
    "2026年{cat}推荐：这{tool_count}款{tool_type}让你效率翻倍",
    "{cat}哪个好用？实测{tool_count}款{tool_type}对比",
    "免费{cat}推荐：{tool_count}个不用花钱的{tool_type}",
    "新手必看：{tool_count}款{cat}推荐，从入门到精通",
    "{cat}排行榜{tool_year}：{tool_count}款{tool_type}横向对比",
    "还在手动{task}？试试这{tool_count}个{cat}推荐",
    "{cat}怎么选？{tool_count}款热门{tool_type}深度评测",
    "打工人必备：{tool_count}款{cat}推荐，告别{task}焦虑",
    "学生党福音：免费{cat}推荐，{task}不再头疼",
    "自媒体人都在用的{tool_count}款{cat}推荐",
    "AI{cat}工具大横评：{tool_count}款{tool_type}谁最强？",
    "企业级{cat}推荐：{tool_count}款{tool_type}提升团队效率",
    "{cat}推荐：{tool_count}个{tool_year}年必试的{tool_type}",
    "从小白到高手：{cat}推荐+{task}实操指南",
    "省钱攻略：{cat}免费{tool_count}连招，不花一分钱搞定{task}",
    "国外{cat} vs 国产{tool_type}：{tool_count}款实测告诉你选哪个",
    "{tool_year}年{cat}推荐清单：这{tool_count}款{tool_type}值得收藏",
    "效率提升{tool_count}倍！{cat}推荐合集来了",
    "别再纠结了！{cat}推荐就看这一篇就够了",
    "{cat}推荐终极指南：{tool_count}个{tool_type}满足所有{task}需求",
]

categories = [
    {"cat":"AI写作工具","task":"写文章","tool_type":"写作工具","tool_count":5,"tools":[
        {"name":"ChatGPT","desc":"OpenAI出品，通用写作能力最强。不管是写公众号推文、产品文案还是学术论文，都能给出质量不错的初稿。支持多轮对话优化，中文能力近两年进步很大。","merit":"质量最高,创意性强","weakness":"免费版有次数限制,高峰期响应慢","scene":"适合需要高质量原创内容的写作者，尤其自媒体运营和市场营销人员"},
        {"name":"Claude","desc":"Anthropic开发，长文本处理能力突出。一次能读20万字，适合写长篇报告、整理会议纪要、分析PDF文档。写作风格更自然流畅，AI味道较轻。","merit":"长文本强,语言自然","weakness":"国内需要特殊方式访问,不支持联网搜索","scene":"适合论文写作、长报告撰写、文档分析整理"},
        {"name":"Kimi","desc":"月之暗面出品的国产AI，长文本能力对标Claude。支持联网搜索，可以读取网页链接直接总结内容。中文写作流畅，适合国内用户日常使用。","merit":"免费使用,支持联网,中文优秀","weakness":"生成长文本偶尔断掉,高峰期排队","scene":"适合日常写作、资料整理、新闻摘要、学生写作业"},
        {"name":"通义千问","desc":"阿里云旗下大模型，整合了阿里生态资源。写作、翻译、代码生成都不错，还有个优势是和钉钉、夸克等阿里系产品深度打通。","merit":"免费,生态整合好,多场景","weakness":"长文逻辑偶尔跑偏,生图功能一般","scene":"适合阿里生态用户、钉钉办公场景、电商文案写作"},
        {"name":"豆包","desc":"字节跳动推出的AI助手，响应速度很快。日常聊天、写作、翻译都够用，多端同步做得好。适合轻度AI使用者入门。","merit":"免费,速度快,多端同步","weakness":"创意写作较弱,专业深度不够","scene":"适合轻度AI用户、碎片化写作、快速查资料"},
    ]},
    {"cat":"AI绘画工具","task":"做图","tool_type":"绘画工具","tool_count":5,"tools":[
        {"name":"Midjourney","desc":"目前公认出图质量最高的AI绘画工具，艺术感和细节表现力一流。需要通过Discord使用，上手有一点门槛。V6版本后对手部等细节处理大幅提升。","merit":"画质天花板,风格多样,社区活跃","weakness":"付费使用,需Discord,生成速度中等","scene":"适合对画面质量要求高的设计师、艺术家、品牌视觉创作"},
        {"name":"Stable Diffusion","desc":"开源免费的AI绘画模型，可以装在自己电脑上跑。插件生态丰富，ControNet、LoRA等玩法很多。自由度极高但需要一些技术基础。","merit":"完全开源,可本地部署,插件多","weakness":"需要配置显卡,学习成本高,出图需要调教","scene":"适合有技术基础、追求定制化、需要批量生成图片的用户"},
        {"name":"DALL·E 3","desc":"OpenAI推出的图像生成工具，对文字的理解力最强。你说「一只戴墨镜的猫在喝咖啡」，它能准确生成。和ChatGPT深度集成，对话式生图很方便。","merit":"文字理解力最强,对话式操作,细节准确","weakness":"付费,风格不如MJ丰富,版权受限","scene":"适合需要精准按描述生成图像、不喜欢复杂Prompt的用户"},
        {"name":"通义万相","desc":"阿里推出的国产AI绘画工具，免费使用。支持文生图、图生图、风格转换等功能。中文Prompt理解好，国风、二次元等本土风格表现不错。","merit":"免费,中文理解好,本土风格丰富","weakness":"写实风格不如MJ,出图质量有波动","scene":"适合国内用户日常作图、电商素材、社交媒体配图"},
        {"name":"文心一格","desc":"百度基于文心大模型推出的AI绘画平台。免费额度较大，支持多种画风。和百度搜索深度整合，搜图+生成一站式解决。","merit":"免费额度大,风格多样,中文优化","weakness":"复杂场景处理弱,细节精细度一般","scene":"适合需要大量配图的内容创作者、教育工作者、个人爱好者"},
    ]},
    {"cat":"AI视频工具","task":"剪视频","tool_type":"视频工具","tool_count":5,"tools":[
        {"name":"Sora","desc":"OpenAI的视频生成模型，能根据文字描述生成一段视频，画面连贯性和物理合理性令人惊艳。目前还在逐步开放中。","merit":"画质领先,连贯性强,理解力好","weakness":"尚未完全开放,生成时间长,价格高","scene":"适合视频创意预演、概念验证、广告分镜制作"},
        {"name":"Runway","desc":"专业级AI视频工具，集成了视频生成、编辑、特效等多种功能。Gen-3模型生成质量高，支持视频到视频转换、运动笔刷等进阶功能。","merit":"功能全面,专业级别,持续更新","weakness":"价格较高,学习曲线陡峭","scene":"适合专业视频制作人、广告公司、电影前期制作"},
        {"name":"可灵","desc":"快手推出的AI视频生成工具，在国产产品中表现突出。支持文生视频和图生视频，中文理解自然，国内用户使用方便。","merit":"国产领先,免费试用,效果好","weakness":"生成时长有限,高峰期排队","scene":"适合短视频创作者、社交媒体运营、个人创意表达"},
        {"name":"Pika","desc":"轻量级AI视频生成工具，界面简洁易上手。支持文字/图片生成视频、视频风格转换，被很多社交媒体博主使用。","merit":"简单易用,社区活跃,更新快","weakness":"视频时长偏短,复杂场景表现一般","scene":"适合短视频创作者、社交媒体内容制作"},
        {"name":"剪映","desc":"字节跳动旗下的视频剪辑工具，AI功能包括自动字幕、智能配音、AI调色、数字人等。免费且功能强大，是目前国内使用最广的视频剪辑工具之一。","merit":"免费,功能全面,AI字幕好用,模板丰富","weakness":"高级特效需付费,非专业级调色","scene":"适合短视频创作、vlog制作、自媒体日常剪辑"},
    ]},
    {"cat":"AI编程工具","task":"写代码","tool_type":"编程助手","tool_count":5,"tools":[
        {"name":"GitHub Copilot","desc":"微软/GitHub推出的AI编程助手，深度集成VS Code、JetBrains等主流IDE。代码补全智能，能根据注释自动生成函数。是程序员中使用率最高的AI工具之一。","merit":"IDE集成好,补全精准,生态完善","weakness":"收费,偶尔生成有bug的代码","scene":"适合所有编程语言的日常开发工作"},
        {"name":"Cursor","desc":"基于VS Code深度定制的AI-first编辑器。不仅能补全代码，还能通过对话修改整个文件、调试、解释代码。被很多开发者称为「下一代编辑器」。","merit":"AI体验最好,对话式编程,免费额度","weakness":"部分插件兼容性问题,更新频繁","scene":"适合追求效率的开发者、全栈工程师"},
        {"name":"Claude Code","desc":"Anthropic推出的命令行AI编程工具，直接在终端中使用。能理解整个项目结构，进行跨文件重构、修复bug、写测试。目前程序员圈口碑极佳。","merit":"代码理解力强,跨文件操作,上下文大","weakness":"命令行门槛,API付费","scene":"适合后端开发、架构重构、自动化脚本编写"},
        {"name":"通义灵码","desc":"阿里出品的免费AI编程插件，支持VS Code和JetBrains。中文注释理解好，生成Java/Go/Python代码质量不错。","merit":"完全免费,中文友好,阿里生态","weakness":"前端代码稍弱,复杂逻辑处理一般","scene":"适合Java/Go开发者、阿里云用户、学生"},
        {"name":"v0.dev","desc":"Vercel推出的AI界面生成工具，用自然语言描述就能生成前端界面代码。基于React/Next.js，生成的代码可以直接部署。","merit":"前端效率极高,代码可直接用,免费","weakness":"只支持前端,复杂交互需手动调整","scene":"适合前端开发、原型快速搭建、独立开发者"},
    ]},
    {"cat":"AI办公工具","task":"做表格","tool_type":"办公工具","tool_count":5,"tools":[
        {"name":"Notion AI","desc":"Notion内置的AI写作和整理功能。能帮你写会议纪要、总结文档、生成待办事项、翻译内容。和Notion知识库深度整合，使用无缝。","merit":"与知识库整合,多功能,体验流畅","weakness":"需付费Notion账号,中文优化一般","scene":"适合用Notion做知识管理的团队和个人"},
        {"name":"Gamma","desc":"AI驱动的演示文稿和文档生成工具。输入一句话主题，自动生成排版精美的PPT。支持实时协作、嵌入多媒体、数据可视化。","merit":"出PPT极快,设计精美,支持协作","weakness":"深度定制需要手动调整,付费版才去水印","scene":"适合经常做PPT的职场人、教师、创业者路演"},
        {"name":"秒出PPT","desc":"国产AI PPT工具，输入标题自动生成大纲和完整PPT。模板丰富偏中国风，支持导出PPTX格式直接使用。","merit":"国产,中文模板多,免费额度","weakness":"AI生成内容有时偏泛,设计不如手动精细","scene":"适合国内职场汇报、教学课件、项目答辩"},
        {"name":"Grammarly","desc":"AI英语写作助手，能实时检查语法、拼写、标点，还能根据语境给出风格和语气建议。浏览器插件覆盖几乎所有网页输入框。","merit":"英语纠错最强,全平台覆盖,实时","weakness":"免费版功能有限,中文不支持","scene":"适合需要用英语写作的所有人"},
        {"name":"通义听悟","desc":"阿里推出的AI会议助手，能实时将语音转文字、生成会议摘要、提取待办事项。支持中英文，接入钉钉和阿里云盘。","merit":"免费,转写准确,自动摘要,钉钉集成","weakness":"多人混音识别有误差,专业词汇需训练","scene":"适合开会频繁的职场人、记者采访、学生听课"},
    ]},
    {"cat":"AI音频工具","task":"做音乐","tool_type":"音频工具","tool_count":5,"tools":[
        {"name":"Suno","desc":"目前最火的AI音乐生成工具，输入歌词和风格提示就能生成完整的歌曲。V4版本音质大幅提升，甚至可以生成广播级音乐。","merit":"生成质量最高,操作简单,风格多样","weakness":"付费,版权归属模糊,偶尔生成失败","scene":"适合音乐爱好者、短视频配乐、独立音乐人灵感获取"},
        {"name":"ElevenLabs","desc":"AI语音合成领域的天花板。能生成极其自然的语音，支持多语言和声音克隆。很多YouTube博主和播客作者用它来做配音。","merit":"语音最自然,多语言,声音克隆","weakness":"付费,免费版字数限制","scene":"适合视频配音、有声书制作、播客录制"},
        {"name":"Udio","desc":"由前Google DeepMind研究员创立的AI音乐平台。音质优秀，支持人声+伴奏分离生成，社区活跃。","merit":"音质好,社区活跃,创意玩法多","weakness":"版权政策待明确,免费额度有限","scene":"适合音乐制作人、创意工作者"},
        {"name":"网易天音","desc":"网易推出的AI音乐创作平台，中文词曲理解好。支持一键生成歌词、编曲、混音，适合华语音乐创作。","merit":"中文优化,免费,词曲一体","weakness":"风格偏流行,高级定制受限","scene":"适合华语音乐创作、demo制作、短视频配乐"},
        {"name":"魔音工坊","desc":"出门问问旗下的AI配音工具，提供数百种音色选择。支持情感调节、语速控制、多角色对话配音。","merit":"音色丰富,中文优秀,情感可控","weakness":"高级音色需付费,导出格式有限","scene":"适合短视频配音、有声内容制作、企业宣传片配音"},
    ]},
    {"cat":"AI Agent","task":"重复操作","tool_type":"Agent平台","tool_count":5,"tools":[
        {"name":"扣子(Coze)","desc":"字节跳动推出的AI Bot搭建平台，零代码就能创建自己的AI智能体。插件生态丰富，能接入飞书、微信、Discord等多渠道。","merit":"零代码,插件多,免费,多平台分发","weakness":"复杂逻辑需学习,企业版收费","scene":"适合想搭建AI客服、个人助理、社群机器人的用户"},
        {"name":"Dify","desc":"开源的LLM应用开发平台，支持可视化的AI应用搭建。提供RAG、Agent、工作流等能力，可私有部署。","merit":"开源,可视化,可私有部署","weakness":"需要服务器,中小团队部署有门槛","scene":"适合企业AI应用搭建、开发者构建AI工作流"},
        {"name":"AutoGPT","desc":"开源AI Agent鼻祖，设定目标后自动分解任务、搜索信息、执行操作。代表了AI自动化的未来方向。","merit":"开源,自动化程度高,愿景宏大","weakness":"实际执行不够稳定,消耗token多","scene":"适合AI研究者和极客探索自动化可能性"},
        {"name":"CrewAI","desc":"多AI Agent协作框架，可以定义不同角色的Agent组成团队，模拟公司内部协作流程。","merit":"多Agent协作,角色分工,开源","weakness":"文档更新慢,入门有门槛","scene":"适合企业流程自动化、研发团队AI实验"},
        {"name":"MetaGPT","desc":"模拟软件公司的多Agent框架，能自动完成需求分析、架构设计、编码、测试等软件研发全流程。","merit":"软件工程全流程,开源,学术背景","weakness":"实际产出需人工把关,运行成本高","scene":"适合软件工程研究、自动化代码生成探索"},
    ]},
    {"cat":"免费AI工具","task":"花钱买会员","tool_type":"免费工具","tool_count":5,"tools":[
        {"name":"DeepSeek","desc":"国产开源大模型，数学和推理能力突出。免费使用，API价格极低。Chat界面简洁好用，代码能力不输ChatGPT。","merit":"完全免费,推理强,API便宜","weakness":"高峰期货应慢,联网功能有限","scene":"适合需要高性价比AI的学生、开发者和中小企业"},
        {"name":"豆包","desc":"字节跳动旗下完全免费的AI助手，聊天、写作、翻译都行。响应速度快，手机端体验好，多端同步。","merit":"完全免费,速度快,体验流畅","weakness":"专业能力中等,不够深度","scene":"适合轻度AI用户日常使用、快速查资料"},
        {"name":"Kimi","desc":"月之暗面免费AI助手，长文本处理免费，联网搜索免费。虽然近期加了付费计划，但免费额度仍然足够日常使用。","merit":"长文本免费,联网免费,中文好","weakness":"高峰期排队,部分高级功能收费","scene":"适合需要处理长文档、搜索资料的用户"},
        {"name":"通义千问","desc":"阿里云旗下免费大模型，功能覆盖面广，从写作到编程到图像生成都有。接入钉钉后办公场景体验好。","merit":"免费,功能全面,阿里生态","weakness":"单项能力非最优,长文质量波动","scene":"适合阿里生态用户、综合需求较多的用户"},
        {"name":"Gemini","desc":"Google推出的大模型，免费版能力已经很强。多模态理解好，和Google搜索、Gmail、YouTube等深度整合。","merit":"免费版能力不错,多模态,Google整合","weakness":"国内访问不便,中文不如国产","scene":"适合Google生态用户、需要多模态理解的场景"},
    ]},
]

intros = [
    "作为{cate}的深度用户，这两年我几乎试遍了市面上所有有点名气的{tool_type}。踩过不少坑，也淘到过一些真正好用的宝贝。今天就把我的经验整理出来，帮你省下筛选的时间。",
    "说实话，选{tool_type}这事真不容易。每个都说自己最好，但实际用起来差别很大——有的快但不够准、有的功能多但上手难、有的免费但限制多。这篇文章根据真实使用体验，聊聊哪些值得用。",
    "花了三个多月时间，每天用不同的{tool_type}做{task}，一点点对比记录下来。下面这份测评不含任何广告，纯粹是个人真实感受，希望能帮你找到最趁手的那一款。",
    "你是不是也被{task}搞得焦头烂额？以前我也这样：改文章改到凌晨、找素材找到崩溃。直到开始用{tool_type}，才真正体会到什么叫事半功倍。今天分享几个改变我工作方式的工具。",
    "这一年来AI工具井喷，光{cate}这个方向每个月都有新产品出来。眼花缭乱之下很多人不知道选哪个，这篇我帮你梳理清楚——哪些是真正好用的，哪些只是噱头。",
    "做自媒体几年了，从一开始全部手写手画，到现在AI辅助创作，效率提升了不止一个档次。今天把踩过几十个坑之后筛选出来的{cate}清单分享给大家。",
    "经常被问「有什么好用的{cat}推荐吗？」与其一遍遍回复，不如写篇文章系统地讲讲。以下是我个人筛选后长期在用的几款，各有各的强项。",
    "AI工具越来越多，但「多」不等于「好」。很多工具用一两次就放弃了——要么不够稳，要么生成的用不了。下面这几款是真正经过时间考验留下来的。",
    "无论是写文案还是做设计，今年我都在大量试AI工具。说实话大部分试完就删了，留下这几款一直用到现在。如果你也在找好用的{cat}，这篇应该能帮到你。",
    "从最初对AI将信将疑，到如今离开AI工具干活效率直接减半，这一年多的变化挺大。整理了我日常实际在用的{cat}推荐，从免费到专业级都有。",
]

compares = [
    "横向比较来看，{t1}在{merit1}方面明显占优，尤其适合{scene1}。{t2}虽然在这块不如{t1}，但{merit2}是它的杀手锏，{scene2}的用户会很喜欢。如果你预算有限，{t3}的性价比最高——{merit3}。",
    "对比这{count}款工具：论综合实力{t1}排第一没悬念，{merit1}确实是目前最稳的。但{t2}在{merit2}这个点上做到了极致，特定场景下甚至超过{t1}。{t3}作为免费选手，{merit3}给得相当大方。",
    "价格方面，{t1}最贵但物有所值；{t2}有免费版可以先体验；{t3}则是完全免费。功能上{t1}最全面，{t2}专注细分领域做得很深，{t3}虽然功能精简但基本够用。",
    "从学习成本来看：{t2}上手最容易，几分钟就能开始用；{t1}功能最多但需要花点时间熟悉；{t3}介于两者之间。如果追求「拿来即用」，{t2}是最佳选择。",
    "如果只看{task}这一个维度，{t1}和{t2}表现都不错，差别不大。但考虑到{merit1}和{merit2}的额外优势，选择就清晰了——看你更看重哪个。",
]

usecases = [
    "比如你要{task}，用{t1}大概{time_save}分钟就能搞定，以前可能要花几倍的时间。有个做自媒体朋友说，自从用了{cate}，他每周能多产出三篇内容。",
    "拿我自己的例子来说：之前做一个项目需要连续{task}，原来要花一整天，现在配合{cate}，一上午就搞完了。省下的下午要么休息，要么用来打磨内容。",
    "很多新手担心AI工具太难上手，其实门槛比想象的低。比如{t2}，注册就能直接用，输入你想要的效果，几分钟就能出成品。我让完全不懂{tool_type}的同事试了试，第一次就能用。",
    "企业用户的话，建议优先考虑{t1}。虽然贵一点但稳定性好，不用担心生成一半出问题。个人用户从{t3}开始就够用了，免费额度日常足够。",
    "学生党可以重点关注{t3}，免费且功能不差。写论文、做PPT、整理笔记这些高频需求都能覆盖。我表妹考研期间就用它整理复习资料，效率高了不少。",
]

outros = [
    "总结一下：如果你预算充足且追求品质，{t1}是首选；看重性价比或者想先试试水，从{t3}开始是个不错的选择。想查看更多{cate}对比评测，点击导航回到主页浏览全部工具。",
    "最后建议：不要纠结选「最好」的，而是选「最适合」的。每款工具都有侧重点，根据自己实际{task}需求来选就行。也可以在主页搜索更多{tool_type}，我们收录了60+款AI工具供你对比。",
    "以上推荐基于长期实际使用体验，每款工具都有各自不可替代的优势。建议先试免费版，觉得好用再升级。返回主页查看更多{cate}的详细介绍和使用教程。",
    "好的工具能让你事半功倍，但工具只是辅助，核心还是使用它的人。建议花点时间上手，熟练之后效率提升会让你惊喜。更多AI工具推荐请查看主页的分类导航。",
    "这个领域发展很快，可能下个月又有更厉害的工具出来。建议关注我们的更新，主页会定期补充新的AI工具评测和对比，帮你始终选到当前最好的。",
]

# ── Build articles ──
articles = []
for cat_data in categories:
    cat = cat_data["cat"]
    task = cat_data["task"]
    tool_type = cat_data["tool_type"]
    tools = cat_data["tools"]
    count = len(tools)

    # Generate titles for this category
    my_titles = random.sample(title_templates, min(13, len(title_templates)))

    for i, tpl in enumerate(my_titles):
        title = tpl.format(
            cat=cat, task=task, tool_type=tool_type,
            tool_count=count, tool_year="2026"
        )
        title = title.replace("推荐：", "推荐").replace("免费", "免费")

        intro = random.choice(intros).format(cate=cat, tool_type=tool_type, task=task, cat=cat)
        outro = random.choice(outros).format(cate=cat, task=task, tool_type=tool_type, t1=tools[0]["name"], t3=tools[-1]["name"])
        compare = random.choice(compares).format(
            t1=tools[0]["name"], t2=tools[1]["name"], t3=tools[2]["name"],
            merit1=tools[0]["merit"], merit2=tools[1]["merit"], merit3=tools[2]["merit"],
            scene1=tools[0]["scene"], scene2=tools[1]["scene"],
            count=count, task=task
        )
        usecase = random.choice(usecases).format(
            task=task, t1=tools[0]["name"], t2=tools[1]["name"], t3=tools[2]["name"],
            cate=cat, tool_type=tool_type,
            time_save=random.choice(["5","10","15"])
        )

        # Build tool cards
        tool_cards = ""
        for j, t in enumerate(tools):
            star = "★" * (5 - j) + "☆" * j if j < 3 else "★★★☆☆"
            tool_cards += f"""
      <div class="tool-item" style="margin-bottom:20px;padding:16px;background:#1a1a2e;border-radius:10px">
        <h3 style="color:#d4a574;margin-bottom:4px">{j+1}. {t['name']} {star}</h3>
        <p style="color:#aaa;font-size:14px;line-height:1.7">{t['desc']}</p>
        <p style="font-size:13px;margin-top:8px"><span style="color:#4caf50">✓ 优势：</span>{t['merit']}</p>
        <p style="font-size:13px"><span style="color:#e67e22">△ 不足：</span>{t['weakness']}</p>
        <p style="font-size:13px;color:#58a6ff">🎯 适合：{t['scene']}</p>
      </div>"""

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{title}——{intro[:80]}...">
<meta name="keywords" content="{cat},{tool_type},AI工具">
<title>{title} - AI工具箱</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0d1117;color:#c9d1d9;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.6;padding:20px;max-width:800px;margin:0 auto}}
h1{{font-size:22px;color:#fff;margin-bottom:10px;line-height:1.4}}
h2{{font-size:18px;color:#d4a574;margin:30px 0 16px;border-left:3px solid #d4a574;padding-left:12px}}
h3{{font-size:16px;margin-bottom:4px}}
p{{margin-bottom:14px;color:#aaa;font-size:15px}}
a{{color:#58a6ff}}
.nav{{margin-bottom:20px;font-size:13px}}
.nav a{{color:#8b949e}}
.header{{text-align:center;padding:30px 0 20px;border-bottom:1px solid #30363d;margin-bottom:30px}}
.header .date{{font-size:12px;color:#8b949e;margin-top:8px}}
.compare-box{{background:#1a1a2e;border-radius:10px;padding:20px;margin:20px 0;border:1px solid #30363d}}
.compare-box p{{font-size:14px}}
.cta{{background:linear-gradient(135deg,#1a2332,#1f1a2e);border:1px solid #30363d;border-radius:12px;padding:20px;text-align:center;margin:30px 0}}
.cta a{{display:inline-block;margin:4px 8px;padding:6px 16px;border-radius:20px;background:#d4a574;color:#000;text-decoration:none;font-size:13px;font-weight:600}}
.cta p{{margin-bottom:12px;color:#fff}}
footer{{text-align:center;padding:30px 0;margin-top:40px;border-top:1px solid #30363d;font-size:13px;color:#8b949e}}
footer a{{color:#8b949e}}
@media(max-width:600px){{body{{padding:12px}}h1{{font-size:18px}}}}
</style>
</head>
<body>
<div class="nav"><a href="/">← 返回AI工具箱首页</a> · <a href="/articles/">文章列表</a></div>
<article>
<div class="header">
  <h1>{title}</h1>
  <div class="date">2026年5月 · AI工具箱原创 · 阅读约{random.choice([3,4,5,6])}分钟</div>
</div>

<p>{intro}</p>

<h2>一、为什么你需要{tool_type}</h2>
<p>很多人还在用传统方式{task}，效率低不说，质量也难保证。好的{tool_type}不仅省时间，还能激发灵感、提升产出质量。以下{count}款工具是我在实际工作中反复对比后留下的，按照综合体验排了序。</p>

<h2>二、{cat}详细评测</h2>
{tool_cards}

<h2>三、横向对比</h2>
<div class="compare-box"><p>{compare}</p></div>

<h2>四、实际使用场景</h2>
<p>{usecase}</p>
<p>关键是找到适合自己工作流程的工具。不用贪多，先把一两款用熟练，效率就能明显提升。需要对比更多{tool_type}的话，随时回到主页按分类查找。</p>

<h2>五、总结与推荐</h2>
<p>{outro}</p>

<div class="cta">
  <p>查看更多AI工具评测和推荐</p>
  <a href="/aitools.html">AI工具导航首页</a>
  <a href="/articles/">更多评测文章</a>
</div>
</article>
<footer>
  <p>AI工具箱 © 2026 · <a href="/aitools.html">返回首页</a> · <a href="/articles/">文章列表</a></p>
</footer>
</body>
</html>"""

        slug = title.replace(" ","-").replace("？","").replace("：","-").replace("！","").replace("，","-")[:60]
        fname = f"{slug}-{random.randint(100,999)}.html"
        filepath = os.path.join(OUT, fname)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        articles.append({"title": title, "file": fname, "cat": cat})

    progress = (len(articles) / 100) * 100
    if len(articles) % 10 == 0:
        print(f"Generated: {len(articles)} articles ({progress:.0f}%)")

# ── Generate listing page ──
listing = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI工具评测文章列表 - AI工具箱</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0d1117;color:#c9d1d9;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;padding:20px;max-width:900px;margin:0 auto}
h1{font-size:22px;color:#fff;text-align:center;margin:20px 0;padding-bottom:16px;border-bottom:1px solid #30363d}
.cat-section{margin:30px 0}
.cat-section h2{font-size:18px;color:#d4a574;margin-bottom:12px}
.article-link{display:block;padding:10px 14px;margin:4px 0;background:#161b22;border-radius:8px;color:#c9d1d9;text-decoration:none;font-size:14px;transition:.15s;border:1px solid #30363d}
.article-link:hover{background:#1a2332;border-color:#58a6ff;color:#fff}
.back{text-align:center;margin-top:30px}
.back a{color:#58a6ff}
.cat-badge{display:inline-block;padding:2px 8px;border-radius:8px;font-size:10px;margin-right:6px;background:rgba(88,166,255,0.1);color:#58a6ff}
</style>
</head>
<body>
<h1>AI工具评测文章 · 共100篇</h1>
"""

cat_groups = {}
for a in articles:
    cat_groups.setdefault(a["cat"], []).append(a)

for cat, arts in cat_groups.items():
    listing += f'<div class="cat-section"><h2>{cat}</h2>'
    for a in arts:
        listing += f'<a class="article-link" href="{a["file"]}"><span class="cat-badge">{cat}</span>{a["title"]}</a>\n'
    listing += '</div>'

listing += """
<div class="back"><a href="/aitools.html">← 返回AI工具箱首页</a></div>
</body></html>
"""

with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(listing)

print(f"\nDone! {len(articles)} articles + listing page in: {OUT}")
