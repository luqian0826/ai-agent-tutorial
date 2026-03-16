# pages/day3_competitor_analysis.py
import streamlit as st
import pandas as pd
import json
import signal
import sys

st.set_page_config(
    page_title="竞品分析",
    page_icon="📊",
    layout="wide"
)

st.title("📊 竞品分析系统")

# 检查PyTorch是否可用
try:
    import torch
    pytorch_available = True
except (ImportError, OSError) as e:
    pytorch_available = False
    st.error("❌ PyTorch未正确安装或版本不兼容")
    st.warning("⚠️ 竞品分析功能需要PyTorch。你的Python版本(3.13)太新，PyTorch还不支持。")
    st.info("💡 解决方案：降级Python到3.10或3.11版本")
    st.stop()

# 延迟导入分析系统，避免页面加载时的错误
try:
    from day2_competitor_analysis import CompetitorAnalysisSystem
except Exception as e:
    st.error(f"❌ 导入分析系统失败：{str(e)}")
    st.warning("⚠️ 这可能是由于PyTorch版本兼容性问题。")
    st.info("💡 请降级Python到3.10或3.11版本以获得完整功能支持。")
    st.stop()

# 初始化分析系统（不使用缓存以避免CrewAI冲突）
if 'analysis_system' not in st.session_state:
    try:
        st.session_state.analysis_system = CompetitorAnalysisSystem()
        system_initialized = True
    except Exception as e:
        st.error(f"❌ 初始化分析系统失败：{str(e)}")
        st.info("💡 提示：这可能是PyTorch版本兼容性问题。请降级Python到3.10或3.11版本。")
        system_initialized = False
else:
    system_initialized = True

system = st.session_state.get('analysis_system')

# 侧边栏
with st.sidebar:
    st.header("⚙️ 分析设置")

    # 单个产品分析
    st.subheader("单个产品分析")
    product_name = st.text_input("产品名称", placeholder="例如：iPhone 15")

    if st.button("开始分析"):
        if not system_initialized:
            st.error("❌ 分析系统未初始化，请刷新页面重试")
        elif product_name:
            status_placeholder = st.empty()
            status_placeholder.info(f"🔄 正在分析 '{product_name}'，请稍候...")

            try:
                # 添加进度显示
                with st.spinner(f"正在分析 {product_name}..."):
                    result = system.analyze_product(product_name)
                    st.session_state.analysis_result = result

                status_placeholder.success(f"✅ 分析完成：{product_name}")

            except Exception as e:
                status_placeholder.error(f"❌ 分析失败：{str(e)}")
                st.error(f"详细错误：{str(e)}")
                # 添加失败记录到session state
                st.session_state.analysis_result = {
                    "product_name": product_name,
                    "status": "failed",
                    "error": str(e),
                    "analysis_date": pd.Timestamp.now().isoformat()
                }

        else:
            st.warning("请输入产品名称")

    # 批量分析
    st.subheader("批量分析")
    batch_products = st.text_area(
        "产品列表（每行一个）",
        placeholder="iPhone 15\nSamsung Galaxy S24\nXiaomi 14"
    )

    if st.button("批量分析"):
        if not system_initialized:
            st.error("❌ 分析系统未初始化，请刷新页面重试")
        elif batch_products:
            products = [p.strip() for p in batch_products.split('\n') if p.strip()]
            results = []

            status_placeholder = st.empty()
            status_placeholder.info(f"🔄 开始批量分析 {len(products)} 个产品...")

            for i, product in enumerate(products, 1):
                try:
                    with st.spinner(f"[{i}/{len(products)}] 正在分析 {product}..."):
                        result = system.analyze_product(product)
                        results.append(result)
                except Exception as e:
                    results.append({
                        "product_name": product,
                        "status": "failed",
                        "error": str(e),
                        "analysis_date": pd.Timestamp.now().isoformat()
                    })

            st.session_state.batch_results = results
            status_placeholder.success(f"✅ 批量分析完成：{len(products)} 个产品")

        else:
            st.warning("请输入产品列表")

# 显示分析结果
if 'analysis_result' in st.session_state:
    st.divider()
    st.header("📋 分析结果")

    result = st.session_state.analysis_result

    # 调试信息
    with st.expander("🔍 调试信息"):
        st.json(result)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("产品名称", result.get("product_name", "N/A"))
        status = result.get("status", "unknown")
        status_label = "✅ 成功" if status == "completed" else "❌ 失败"
        st.metric("分析状态", status_label)

    with col2:
        analysis_date = result.get("analysis_date", "N/A")
        if analysis_date and analysis_date != "N/A":
            analysis_date = analysis_date[:19]
        st.metric("分析时间", analysis_date)

    if result.get("status") == "completed":
        st.subheader("详细分析")
        # 获取分析结果
        analysis_result = result.get("analysis_result", "")

        if isinstance(analysis_result, str):
            # 如果是字符串（Markdown格式），使用st.markdown显示
            st.markdown(analysis_result)
        elif isinstance(analysis_result, dict):
            # 如果是字典，使用st.json显示
            st.json(analysis_result)
        else:
            # 其他类型，转换为字符串显示
            st.markdown(str(analysis_result))

        # 显示报告文件路径
        if analysis_result:
            st.info(f"📄 完整报告已保存到 competitor_reports 目录")

    else:
        st.error(f"分析失败：{result.get('error', 'Unknown error')}")

# 显示批量分析结果
if 'batch_results' in st.session_state:
    st.divider()
    st.header("📊 批量分析结果")

    results = st.session_state.batch_results

    # 汇总统计
    success_count = sum(1 for r in results if r.get("status") == "completed")
    failed_count = sum(1 for r in results if r.get("status") == "failed")

    col1, col2, col3 = st.columns(3)
    col1.metric("总产品数", len(results))
    col2.metric("成功", success_count)
    col3.metric("失败", failed_count)

    # 详细表格
    df_data = []
    for result in results:
        analysis_date = result.get("analysis_date", "N/A")
        if analysis_date and analysis_date != "N/A":
            analysis_date = analysis_date[:19]

        df_data.append({
            "产品名称": result.get("product_name", "N/A"),
            "状态": result.get("status", "N/A"),
            "分析时间": analysis_date,
            "错误信息": result.get("error", "")[:50] if result.get("error") else ""
        })

    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True)

# 添加Python版本提示
st.divider()
st.info(f"📌 当前Python版本：{sys.version.split()[0]} | PyTorch状态：{'✅ 已安装' if pytorch_available else '❌ 未安装/不兼容'}")
if not pytorch_available:
    st.warning("⚠️ 建议降级Python到3.10或3.11版本以获得完整功能支持。")