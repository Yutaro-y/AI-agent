import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
import streamlit as st
from langchain.schema import HumanMessage, AIMessage, SystemMessage
import asyncio
import json

load_dotenv()

# OpenAIクライアントを生成
llm = ChatOpenAI(
    model="gpt-4o-mini",  # 適切なモデル名を指定
    temperature=0.2,
    streaming=True,
    openai_api_key=os.getenv('OPENAI_API_KEY')  # 環境変数からAPIキーを取得
)


async def main():
    with open("/home/user/projects/lang-stream-mcp/mcp_config.json", "r") as file:
        config = json.load(file)
    
    print("json load done")
    mcp_client = MultiServerMCPClient(config["mcpServers"])
    print("MultiserverMCPClient initialize done")
    all_tools = await mcp_client.get_tools()
    print("MultiserverMCPClient get_tools done")
    print(all_tools)
    
    # エージェントを作成
    agent = create_react_agent(llm, all_tools) 
   
    #Streamlitの処理開始
    # # セッションステートを初期化
    if "messages" not in st.session_state:
        st.session_state.messages = [SystemMessage(content="あなたはコンピューティングやネットワーク技術に詳しいスペシャリストです。ツールを実行するときはその理由と途中の考察を必ず書いてください。繰り返し問題に対処して期待通りの結果が得られない場合は一度中断して状況をまとめてください。")]
        
    # メッセージ履歴を表示
    for message in st.session_state.messages:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
    
    print("Display message history done")
    
    # ユーザーからの入力を受け取る
    if prompt := st.chat_input("ここに入力してください:"):
        # ユーザーのメッセージを履歴に追加
        user_message = HumanMessage(content=prompt)
        st.session_state.messages.append(user_message)
        print("append user-message done")

        # チャットメッセージとして表示
        with st.chat_message("user"):
            st.markdown(prompt)
            print("print user message done")    
        #チャットボットの応答
        with st.chat_message("assistant"):
            expander = st.expander("tool use process")
            message_placeholder = st.empty()  # プレースホルダーを作成
            contents = ""
            tool_outputs = [] #ツール出力の初期化(初期コードはここで定義)
            recursion_limit = 50 #エージェントの実行回数の上限設定
            #stream = agent.stream({"messages": st.session_state.messages}, stream_mode=["updates","messages"])
            
            async for event in agent.astream_events({"messages": st.session_state.messages}, {"recursion_limit": recursion_limit}, version="v1"):
                # メッセージの表示
                if event["event"] == "on_chat_model_stream":
                    content = event["data"]["chunk"].content
                    if content:
                        contents += content
                        message_placeholder.markdown(contents)
                        
                # ツール利用の開始
                elif event["event"] == "on_tool_start":
                    tool_outputs = [] #ツール出力を初期化
                    tmp = f"#### Start using the tool : {event['name']}  \nInputs: {event['data'].get('input')}"
                    tool_outputs.append(tmp)
                    expander.markdown(tmp)
                # ツール利用の終了
                elif event["event"] == "on_tool_end":
                    tmp = f"#### Finish using the tool : {event['name']}  \nOutput : {event['data'].get('output')}"
                    tool_outputs.append(tmp)
                    expander.markdown(tmp)
               
            st.session_state.messages.append({"role": "assistant", "content": contents, "tool": tool_outputs})

if __name__ == "__main__":
    asyncio.run(main())

