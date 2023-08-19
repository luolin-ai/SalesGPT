🤖 SalesGPT - 您的情境感知 AI 销售助理
此存储库演示了使用 LLM 实现上下文感知 AI 销售助手。

SalesGPT 是上下文感知的，这意味着它可以了解它处于销售对话的哪个部分并采取相应的行动。 此外，SalesGPT 可以访问工具，例如您自己的预定义产品知识库，从而大大减少幻觉！

我们在此实现中利用了langchain库，特别是自定义代理配置，并受到BabyAGI架构的启发。

我们的愿景：打造最好的开源自主销售代理
我们正在构建 SalesGPT，为您最好的自主销售代理提供支持。因此，我们很想了解更多关于您正在构建的用例，这些用例将推动 SalesGPT 开发路线图。

如果您希望我们更好地满足您的需求，请填写我们的 45 秒 SalesGPT 用例调查

如果您寻求帮助建立您的自主销售代理
请发送电子邮件给存储库作者。

🔴 最新消息
销售代理现在可以利用工具，例如在产品目录中查找产品！
演示：来自Crusty AI的出站勘探：一种新的销售方式？🤔
Crusty AI 销售代理电话演示 - 由 SalesGPT 提供支持


快速入门
import os
from salesgpt.agents import SalesGPT
from langchain.chat_models import ChatOpenAI

os.environ['OPENAI_API_KEY'] = 'sk-xxx' # fill me in

llm = ChatOpenAI(temperature=0.4)
                            
sales_agent = SalesGPT.from_llm(llm, use_tools=True, verbose=False,
                            product_catalog = "examples/sample_product_catalog.txt",
                            salesperson_name="Ted Lasso",
                            salesperson_role="Sales Representative",
                            company_name="Sleep Haven",
                            company_business='''Sleep Haven 
                            is a premium mattress company that provides
                            customers with the most comfortable and
                            supportive sleeping experience possible. 
                            We offer a range of high-quality mattresses,
                            pillows, and bedding accessories 
                            that are designed to meet the unique 
                            needs of our customers.'''
                            )
sales_agent.seed_agent()
sales_agent.determine_conversation_stage() # optional for demonstration, built into the prompt

# agent 
sales_agent.step()

# user
user_input = input('Your response: ') # Yea, sure
sales_agent.human_step(user_input)

# agent
sales_agent.determine_conversation_stage() # optional for demonstration, built into the prompt
sales_agent.step()

# user
user_input = input('Your response: ') # What pricing do you have for your mattresses?
sales_agent.human_step(user_input)

# agent
sales_agent.determine_conversation_stage() # optional for demonstration, built into the prompt
sales_agent.step()
对话阶段： 简介：通过介绍自己和您的公司来开始对话。

想：我需要使用工具吗？No
Ted Lasso：你好，我叫Ted Lasso，我代表Sleep Haven打电话。我们是一家优质的床垫公司，为客户提供最舒适和支持性的睡眠体验。我想知道您是否有兴趣了解更多关于我们的产品以及它们如何改善您的睡眠？

用户：是的，当然

对话阶段： 价值主张：简要说明您的产品/服务如何使潜在客户受益。

想：我需要使用工具吗？没有
泰德·拉索：很高兴听到这个消息！我们的床垫经过专门设计，可根据您的体型进行轮廓塑造，提供完美的支撑和舒适度，让您睡个好觉。此外，它们采用经久耐用的优质材料制成。您想了解更多关于我们不同的床垫选择吗？

用户：你们的床垫定价是多少？

想：我需要使用工具吗？是的 - > AI 代理在此处使用工具。
操作：产品搜索
操作床垫的
输入定价 观察：Sleep Haven 提供三种床垫：经典和谐弹簧床垫 1，299 美元，毛绒宁静竹床垫 2，599 美元，豪华云舒适记忆泡沫床垫 999 美元。可用的尺寸因床垫而异。
Ted Lasso：Sleep Haven提供三种不同价位的床垫。经典和谐弹簧床垫售价1，299美元，豪华宁静竹床垫售价2，599美元，豪华云舒适记忆泡沫床垫售价999美元。价格可能会因您选择的尺寸而异。您想了解更多关于每张床垫的具体尺寸和功能的信息吗？

产品知识库
AI 销售代理可以访问工具，例如您的内部产品知识库。 这允许代理商只谈论您自己的产品，并显着减少幻觉。

了解上下文
AI 销售代理了解对话阶段（您可以根据需要定义自己的阶段）：

简介：通过介绍自己和您的公司来开始对话。
资格： 通过确认潜在客户是否是与您的产品/服务交谈的合适人选来限定他们。
价值主张：简要说明您的产品/服务如何使潜在客户受益。
需求分析：提出开放式问题，以发现潜在客户的需求和痛点。
解决方案演示：根据潜在客户的需求，将您的产品/服务展示为可以解决其痛点的解决方案。
异议处理：解决潜在客户可能对您的产品/服务提出的任何异议。
关闭：通过提出下一步来要求出售。
结束对话：用户不想继续对话，因此请结束通话。
因此，该代理可以与潜在客户进行自然的销售对话，并根据对话阶段行事。因此，此笔记本演示了如何使用 AI 来自动化销售开发代表活动，例如出站销售电话。

建筑


安装
确保你有python 3.10+并运行：

pip install -r requirements.txt

创建文件并通过指定一行将 Open AI 密钥放在那里：.env

OPENAI_API_KEY=sk-xxx

用点子安装

pip install salesgpt

试试看
要了解与 AI 销售代理的对话，您可以运行：

python run.py --verbose True --config examples/example_agent_setup.json

从您的终端。

联系我们
如有疑问，可以联系存储库作者。

关注我@FilipMichalsky

销售GPT路线图
[高优先级]提高解析器问题的可靠性 这里 和 这里
在此处添加 OpenAI 函数代理问题的示例实现
在此处添加对多个工具问题的支持
为需要线性遍历的阶段添加代理控制器，而不会在此处跳过问题
添加以根据矢量距离选择工具，以完成所需的takstoo_getter
代理应该拥有哪些工具？（例如，搜索互联网的能力）
添加销售代理与您网站上的 AI 插件交互的功能 （.well-known/ai-plugin.json） - 添加在用户中断代理时停止生成的功能
- 添加一个矢量存储以合并真实的产品知识库，而不是组成它的LLM。

- 销售代理可以提供的产品/服务的知识库（因此LLM不会弥补）

- 将LLM链（线性工作流程）转换为代理（根据用户的输入决定做什么）

贡献
强烈鼓励贡献！请分叉并提交 PR。
