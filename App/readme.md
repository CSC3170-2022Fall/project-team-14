# 使用VS Code和Flask框架开发基于Python的Web应用

## Windows

1. 以管理员身份运行cmd
2. 进入项目目录
    如果是GitHub项目，进入GitHub在本地的目录，如:
    C:\Users\xxx\github-classroom\CSC3170-2022Fall\project-team-13\
3. 进入虚拟环境
    `.venv\Scripts\activate`
    ![alt text](/material/images/vitual_create.png)
4. 虚拟环境如下, 输入`pip install Flask`
    ![alt text](/material/images/vitual_env.png)
5. 打开VS code，使用快捷键：
    `Ctrl+Shift+P`
6. 打开VS Code命令窗口。选择：
    `Python: Select Interpreter`
    ![alt text](/material/images/interpreter.png)
7. 在弹出的下拉框中选择创建的虚拟环境。
    ![alt text](/material/images/select.png)
8. 打开VS code终端，输入:
    `python -m pip install flask`
9. 进入App目录，此时就可以运行flask了。这里我们直接运行app.py文件：
    ![alt text](/material/images/run.png)
10. 按住Ctrl+单击 http://127.0.0.1:5000 , 进入我们的网页。