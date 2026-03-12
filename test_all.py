"""
AI Agent Tutorial - 完整测试脚本
测试所有功能模块
"""
import os
import sys
import subprocess
from pathlib import Path


def print_header(title):
    """打印标题"""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def print_status(status, message):
    """打印状态"""
    icon = "✅" if status else "❌"
    print(f"{icon} {message}")


def check_env():
    """检查环境配置"""
    print_header("环境检查")

    # 检查Python版本
    if sys.version_info >= (3, 9):
        print_status(True, f"Python版本: {sys.version}")
    else:
        print_status(False, f"Python版本过低: {sys.version} (需要3.9+)")
        return False

    # 检查.env文件
    if Path(".env").exists():
        print_status(True, ".env文件存在")
    else:
        print_status(False, ".env文件不存在")
        print("   请复制 .env.example 为 .env 并设置API密钥")
        return False

    # 检查API密钥
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("DEEPSEEK_API_KEY", "")

    if api_key and api_key != "your_api_key_here":
        print_status(True, "API密钥已配置")
    else:
        print_status(False, "API密钥未配置")
        return False

    return True


def check_dependencies():
    """检查依赖"""
    print_header("依赖检查")

    required_packages = [
        "langchain",
        "crewai",
        "chromadb",
        "aiohttp",
        "pandas",
        "numpy"
    ]

    all_ok = True
    for package in required_packages:
        try:
            __import__(package)
            print_status(True, f"{package} 已安装")
        except ImportError:
            print_status(False, f"{package} 未安装")
            all_ok = False

    return all_ok


def test_file(filename, description):
    """测试单个文件"""
    print(f"\n📝 测试: {description}")
    print(f"   文件: {filename}")

    try:
        result = subprocess.run(
            [sys.executable, filename],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            print_status(True, f"{description} 测试通过")
            return True
        else:
            print_status(False, f"{description} 测试失败")
            if result.stderr:
                print(f"   错误: {result.stderr[:200]}")
            return False

    except subprocess.TimeoutExpired:
        print_status(False, f"{description} 测试超时")
        return False
    except Exception as e:
        print_status(False, f"{description} 测试异常: {str(e)}")
        return False


def interactive_test():
    """交互式测试"""
    print_header("交互式测试")

    print("\n选择要测试的模块:")
    print("1. Day 1: 基础Agent")
    print("2. Day 2: 网络搜索工具")
    print("3. Day 2: 文件读写工具")
    print("4. Day 2: 数据分析工具")
    print("5. Day 2: 记忆系统")
    print("6. Day 2: 记忆增强Agent")
    print("7. Day 2: 多Agent团队")
    print("8. Day 2: 竞品分析系统")
    print("9. Day 2: 异步处理")
    print("10. Day 2: 缓存机制")
    print("0. 运行所有测试")
    print("q. 退出")

    choice = input("\n请输入选项 (0-10, q): ").strip()

    test_map = {
        "1": ("day1_agent.py", "Day 1 基础Agent"),
        "2": ("day2_tools.py", "网络搜索工具"),
        "3": ("day2_file_tools.py", "文件读写工具"),
        "4": ("day2_analysis_tools.py", "数据分析工具"),
        "5": ("day2_memory.py", "记忆系统"),
        "6": ("day2_memory_agent.py", "记忆增强Agent"),
        "7": ("day2_team.py", "多Agent团队"),
        "8": ("day2_competitor_analysis.py", "竞品分析系统"),
        "9": ("day2_async.py", "异步处理"),
        "10": ("day2_cache.py", "缓存机制"),
    }

    if choice == "0":
        # 运行所有测试
        print_header("运行所有测试")
        results = []
        for key, (filename, desc) in test_map.items():
            result = test_file(filename, desc)
            results.append((desc, result))

        # 汇总结果
        print_header("测试结果汇总")
        passed = sum(1 for _, r in results if r)
        total = len(results)

        for desc, result in results:
            print_status(result, desc)

        print(f"\n总计: {passed}/{total} 测试通过")

    elif choice in test_map:
        filename, desc = test_map[choice]
        test_file(filename, desc)
    elif choice.lower() == "q":
        print("退出测试")
        return False
    else:
        print("无效选项")

    return True


def main():
    """主函数"""
    print_header("AI Agent Tutorial - 完整测试")
    print("\n欢迎使用AI Agent教程测试系统！")
    print("这个脚本将帮助你测试所有功能模块。\n")

    # 检查环境
    if not check_env():
        print("\n❌ 环境检查失败，请修复后重试")
        return

    # 检查依赖
    if not check_dependencies():
        print("\n❌ 依赖检查失败，请运行: pip install -r requirements.txt")
        return

    # 交互式测试
    while True:
        if not interactive_test():
            break

        again = input("\n是否继续测试？(y/n): ").strip().lower()
        if again != 'y':
            break

    print_header("测试完成")
    print("\n感谢使用！")
    print("如需帮助，请查看 README.md")


if __name__ == "__main__":
    main()