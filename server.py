from fastapi import FastAPI, Request
import requests

app = FastAPI()

@app.post("/github-webhook")
async def handle_github_webhook(request: Request):
    data = await request.json()
    event_type = request.headers.get('X-GitHub-Event')

    if event_type == 'push':
        actor = data['pusher']['name']
        repository = data['repository']['name']
        repository_url = data['repository']['html_url']
        commit_message = data['head_commit']['message']
        commit_url = data['head_commit']['url']

        message = f"{actor} pushed to repository [{repository}]({repository_url})\
\
"
        message += f"Commit: [{commit_message}]({commit_url})"

        send_to_feishu(message)

    elif event_type == 'commit_comment':
        actor = data['comment']['user']['login']
        repository = data['repository']['name']
        repository_url = data['repository']['html_url']
        comment_body = data['comment']['body']
        comment_url = data['comment']['html_url']

        message = f"{actor} commented on repository [{repository}]({repository_url})\
\
"
        message += f"Comment: [{comment_body}]({comment_url})"

        send_to_feishu(message)

    elif event_type == 'star':
        actor = data['sender']['login']
        repository = data['repository']['name']
        repository_url = data['repository']['html_url']

        message = f"{actor} starred repository [{repository}]({repository_url})"

        send_to_feishu(message)

    elif event_type == 'fork':
        actor = data['forkee']['owner']['login']
        repository = data['forkee']['name']
        repository_url = data['forkee']['html_url']

        message = f"{actor} forked repository [{repository}]({repository_url})"

        send_to_feishu(message)

    elif event_type == 'issues':
        actor = data['sender']['login']
        repository = data['repository']['name']
        repository_url = data['repository']['html_url']
        issue_title = data['issue']['title']
        issue_url = data['issue']['html_url']

        message = f"{actor} opened an issue on repository [{repository}]({repository_url})\
\
"
        message += f"Issue: [{issue_title}]({issue_url})"

        send_to_feishu(message)

    elif event_type == 'issue_comment':
        actor = data['comment']['user']['login']
        repository = data['repository']['name']
        repository_url = data['repository']['html_url']
        issue_title = data['issue']['title']
        issue_url = data['issue']['html_url']
        comment_body = data['comment']['body']

        message = f"{actor} commented on issue [{issue_title}]({issue_url}) in repository [{repository}]({repository_url})\
\
"
        message += f"Comment: [{comment_body}]"

        send_to_feishu(message)

    return {"message": "OK"}

def send_to_feishu(message):
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/b2cf824b-9535-41f3-9a33-82df1fd3ba6c"
    headers = {"Content-Type": "application/json"}
    payload = {
        "msg_type": "text",
        "content": {
                        "text": message.replace("\
                                ", "\
                                \
                                ")
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

