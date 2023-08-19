🤖 SalesGPT - 您的上下文感知人工智能销售助手
此存储库演示了使用法学硕士实现上下文感知AI 销售助理。

SalesGPT 具有上下文感知能力，这意味着它可以了解当前处于销售对话的哪个部分并采取相应的行动。此外，SalesGPT 可以访问工具，例如您自己的预定义产品知识库，从而显着减少幻觉！

我们langchain在此实现中利用了该库，特别是自定义代理配置，并受到BabyAGI架构的启发。

我们的愿景：打造最好的开源自主销售代理
我们正在构建 SalesGPT 来为您最好的自主销售代理提供支持。因此，我们很乐意了解有关您正在构建的用例的更多信息，这些用例将推动 SalesGPT 开发路线图。

如果您希望我们更好地满足您的需求，请填写我们的 45 秒SalesGPT 用例调查

如果您在构建自主销售代理方面寻求帮助
请发送电子邮件给存储库作者。

🔴最新消息
销售代理现在可以利用工具，例如在产品目录中查找产品！
演示：Crusty AI 的出站勘探：一种新的销售方式？🤔
Crusty AI 销售代理电话演示 - 由 SalesGPT 提供支持


快速开始
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
对话阶段： 介绍：通过介绍您自己和您的公司来开始对话。

思考：我需要使用工具吗？不
Ted Lasso：您好，我叫 Ted Lasso，我代表 Sleep Haven 致电。我们是一家优质床垫公司，致力于为客户提供最舒适、最具支撑性的睡眠体验。我想知道您是否有兴趣了解更多关于我们的产品以及它们如何改善您的睡眠？

用户： 是的，当然

对话阶段：价值主张：简要解释您的产品/服务如何使潜在客户受益。

思考：我需要使用工具吗？没有
特德·拉索：很高兴听到这个消息！我们的床垫经过专门设计，贴合您的体型，提供完美的支撑和舒适度，让您享受更好的睡眠。此外，它们采用经久耐用的优质材料制成。您想了解更多有关我们不同床垫选择的信息吗？

用户：你们的床垫定价是多少？

思考：我需要使用工具吗？是的 --> AI Agent 在这里使用工具。
行动：ProductSearch
ActionInput 床垫定价
观察：Sleep Haven 提供三种床垫：经典 Harmony 弹簧床垫，售价 1,299 美元；毛绒宁静竹床垫，售价 2,599 美元；豪华云舒适记忆泡沫床垫，售价 999 美元。可用尺寸因床垫而异。
Ted Lasso：Sleep Haven 提供三种不同价位的床垫。经典Harmony弹簧床垫售价1,299美元，毛绒Serenity竹床垫售价2,599美元，豪华云舒适记忆海绵床垫售价999美元。价格可能会根据您选择的尺寸而有所不同。您想了解有关每个床垫的具体尺寸和功能的更多信息吗？

产品知识库
AI 销售代理可以访问工具，例如您的内部产品知识库。这使得代理只能谈论您自己的产品，并显着减少幻觉。

了解背景
AI销售代理了解对话阶段（您可以根据您的需求定义自己的阶段）：

介绍：通过介绍您自己和您的公司来开始对话。
资格：通过确认潜在客户是否是谈论您的产品/服务的合适人选来确定潜在客户的资格。
价值主张：简要解释您的产品/服务如何使潜在客户受益。
需求分析：提出开放式问题以揭示潜在客户的需求和痛点。
解决方案展示：根据潜在客户的需求，展示您的产品/服务作为可以解决他们的痛点的解决方案。
异议处理：解决潜在客户对您的产品/服务可能提出的任何异议。
结束：通过提出下一步行动来要求出售。
结束通话：用户不想继续通话，因此结束通话。
因此，该代理可以与潜在客户进行自然的销售对话，并根据对话阶段采取行动。因此，本笔记本演示了我们如何使用人工智能来自动化销售开发代表活动，例如外拨销售电话。

建筑学


安装
确保你有 python 3.10+ 并运行：

pip install -r requirements.txt

创建.env文件并通过指定一行将您的 Open AI Key 放在那里：

OPENAI_API_KEY=sk-xxx

使用 pip 安装

pip install salesgpt

试试看
要体验与 AI Sales 代理的对话，您可以运行：

python run.py --verbose True --config examples/example_agent_setup.json

从您的终端。

联系我们
如有疑问，您可以联系存储库作者。

通过@FilipMichalsky关注我

SalesGPT 路线图
[高优先级] 提高解析器问题的可靠性（此处和此处）
在此处添加 OpenAI 函数代理问题的示例实现
在此处添加对多个工具问题的支持
添加一个代理控制器，用于需要线性遍历阶段而不会出现跳过问题的情况
添加too_getter根据与需要完成的任务的矢量距离来选择工具
代理应该具备哪些工具？（例如，搜索互联网的能力）
添加销售代理与您网站上的 AI 插件交互的功能 (.well-known/ai-plugin.json) - 添加当用户中断代理时停止生成的功能
- 添加一个矢量存储来合并真实的产品知识库，而不是由法学硕士组成。

- 销售代理可以提供的产品/服务的知识库（因此法学硕士不会弥补）

- 将LLM链（线性工作流程）转换为代理（根据用户的输入决定做什么）

贡献
强烈鼓励贡献！请分叉并提交 PR。
