<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>Did a git pull for {{name}} on {{branch}}</title>
	<style>
		::-moz-selection{background:#b3d4fc;text-shadow:none}::selection{background:#b3d4fc;text-shadow:none}html{padding:30px 10px;font-size:20px;line-height:1.4;color:#737373;background:#f0f0f0;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%}html,input{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif}body{max-width:700px;_width:700px;padding:30px 20px 50px;border:1px solid #b3b3b3;border-radius:4px;margin:0 auto;box-shadow:0 1px 10px #a7a7a7,inset 0 1px 0 #fff;background:#fcfcfc}h1{margin:0 10px;font-size:50px;text-align:center}h1 span{color:#bbb}h3{margin:1.5em 0 .5em}p{margin:1em 0}ul{padding:0 0 0 40px;margin:1em 0}.container{max-width:580px;_width:580px;margin:0 auto}pre.log{position:relative;clear:left;min-height:12px;margin-top:25px;margin-top:1em;padding:15px 0;color:#f1f1f1;font-family:monospace;font-size:12px;line-height:19px;white-space:pre-wrap;word-wrap:break-word;background-color:#222;border:1px solid #ddd;overflow-x:scroll;counter-reset:line-numbering}pre.log p{padding:0 15px 0 55px;margin:0;min-height:16px}pre.log p:hover{background-color:#444!important}pre.log p.highlight{background-color:#666}pre.log p.highlight a{color:#fff}pre.log p a{display:inline-block;text-align:right;min-width:40px;margin-left:-33px;cursor:pointer;text-decoration:none}pre.log p a::before{content:counter(line-numbering);counter-increment:line-numbering;padding-right:1em}
	</style>
	</head>
	<body>
		<div class="container">
			<p>I did a pull of repository <strong>{{name}}</strong> on branch <strong>{{branch}}</strong> on <strong>{{now.strftime('%-d, %b %Y at %-I:%M %p')}}</strong>.</p>
			<p>It generated the following output</p>
			<h3>Output</h3>
			<pre class="log">{{!"".join(["<p><a></a><span>%s</span></p>" % line for line in output])}}</pre>
			<p>with the following console error</p>
			<h3>Error</h3>
			<pre class="log">{{!"".join(["<p><a></a><span>%s</span></p>" % line for line in error])}}</pre>
		</div>
	</body>
</html>