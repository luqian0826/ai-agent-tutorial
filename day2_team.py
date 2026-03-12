# day2_team.py
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
import os
from day2_tools import crewai_web_search_tool
from day2_analysis_tools import DataAnalyzer

load_dotenv()

# 初始化DeepSeek模型
llm = LLM(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.7
)

# ====== 1. 定义Agent角色 ======

# 经理Agent
manager = Agent(
    role="项目经理",
    goal="协调团队成员，确保任务按时高质量完成",
    backstory="""你是一位经验丰富的项目经理，擅长拆解复杂任务、
    分配工作、监控进度和质量。你总是能找到最优的解决方案.""",
    llm=llm,
    verbose=True,
    allow_delegation=True  # 允许委派任务
)

# 研究员Agent
researcher = Agent(
    role="市场研究员",
    goal="收集和分析市场信息，为决策提供数据支持",
    backstory="""你是一位敏锐的市场研究员，擅长通过网络搜索和数据挖掘
    获取有价值的信息。你能够快速筛选和验证信息真实性.""",
    llm=llm,
    tools=[crewai_web_search_tool],  # 使用 CrewAI 兼容的搜索工具
    verbose=True
)

# 分析师Agent
analyst = Agent(
    role="数据分析师",
    goal="分析数据，发现趋势和洞察，生成专业报告",
    backstory="""你是一位资深数据分析师，擅长用Python进行数据分析，
    能够从数据中发现有价值的模式和趋势.""",
    llm=llm,
    verbose=True
)

# 报告员Agent
reporter = Agent(
    role="技术报告员",
    goal="将分析结果整理成清晰、专业的报告",
    backstory="""你是一位专业的技术文档撰写人，擅长将复杂的技术
    分析结果转化为易于理解的报告.""",
    llm=llm,
    verbose=True
)

# ====== 2. 定义任务 ======

# 任务1：信息收集
research_task = Task(
    description="""搜索 {product_name} 的基本信息，包括价格、特点等""",
    expected_output="产品基本信息",
    agent=researcher
)

# 任务2：数据分析
analysis_task = Task(
    description="""基于收集的信息，分析产品的主要特点""",
    expected_output="产品特点分析",
    agent=analyst,
    context=[research_task]
)

# 任务3：报告生成
report_task = Task(
    description="""整合信息，写一份简短的报告，包括产品概述和特点""",
    expected_output="产品分析报告",
    agent=reporter,
    context=[research_task, analysis_task]
)

# ====== 3. 创建团队 ======

# 创建AI团队
ai_team = Crew(
    agents=[manager, researcher, analyst, reporter],
    tasks=[research_task, analysis_task, report_task],
    process=Process.sequential,  # 使用顺序式流程
    verbose=True
)

# ====== 4. 运行团队 ======

def run_competitor_analysis(product_name: str):
    """运行竞品分析"""
    print(f"🚀 开始分析产品: {product_name}")
    print("=" * 60)

    try:
        result = ai_team.kickoff(inputs={"product_name": product_name})

        print("=" * 60)
        print("✅ 分析完成！")
        print("\n📊 分析结果：")
        print(result)

        return result

    except Exception as e:
        print(f"❌ 分析失败: {str(e)}")
        return None

# 测试代码
if __name__ == "__main__":
    print("👥 测试多Agent团队")
    print("=" * 60)

    # 示例：分析某个产品
    result = run_competitor_analysis("iPhone 15")

    if result:
        print("\n" + "=" * 60)
        print("✅ 多Agent团队测试完成")
    else:
        print("\n" + "=" * 60)
        print("⚠️  分析过程中遇到问题，请检查配置和网络连接")