% import re
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>Overview of registered repositories :: iocasts' hook-server</title>
		<style>
			::-moz-selection{background:#b3d4fc;text-shadow:none}::selection{background:#b3d4fc;text-shadow:none}html{padding:30px 10px;font-size:1em;line-height:1.4;color:#737373;background:#f0f0f0;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%}html,input{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif}body{max-width:700px;_width:700px;padding:30px 20px 50px;border:1px solid #b3b3b3;border-radius:4px;margin:0 auto;box-shadow:0 1px 10px #a7a7a7,inset 0 1px 0 #fff;background:#fcfcfc}h1{margin:0 10px;font-size:2em;text-align:center}h1 span{color:#bbb}h3{margin:1.5em 0 .5em}p{margin:1em 0}ul{padding:0 0 0 40px;margin:1em 0}.container{max-width:580px;_width:580px;margin:0 auto}pre.log{position:relative;clear:left;min-height:12px;margin-top:25px;margin-top:1em;padding:15px 0;color:#f1f1f1;font-family:monospace;font-size:12px;line-height:19px;white-space:pre-wrap;word-wrap:break-word;background-color:#222;border:1px solid #ddd;overflow-x:scroll;counter-reset:line-numbering}pre.log p{padding:0 15px 0 55px;margin:0;min-height:16px}pre.log p:hover{background-color:#444 !important}pre.log p.highlight{background-color:#666}pre.log p.highlight a{color:#fff}pre.log p a{display:inline-block;text-align:right;min-width:40px;margin-left:-33px;cursor:pointer;text-decoration:none}pre.log p a::before{content:counter(line-numbering);counter-increment:line-numbering;padding-right:1em}dl{clear:both;overflow:hidden;padding:5px}dt{float:left;clear:left;width:150px;font-weight:bold;text-align:right}dd{margin:0 0 0 10px;padding:0;float:left}.tree{min-height:20px;margin-bottom:20px}.tree li>ul{padding-left:20px;font-weight:normal}.tree ul:first-child{padding:0;margin:0;font-weight:bold}.tree li{list-style:none;list-style-type:none;margin:0 0 0 20px;padding:10px 5px 0 5px;position:relative}.tree>ul>li{margin:0}.tree li::before,.tree li::after{content:'';left:-20px;position:absolute;right:auto}.tree li::before{border-left:1px solid #999;bottom:50px;height:100%;top:0;width:1px}.tree li::after{border-top:1px solid #999;height:20px;top:25px;width:25px}.tree>ul>li::before,.tree>ul>li::after{border:0}.tree li:last-child::before{height:30px}.tree li>div{display:table-cell;padding-left:10px}.tree li>div:first-child{padding-left:0;min-width:150px}.tree li>div.right{width:100%;text-align:right}
		</style>
	</head>
	<body>
		<div class="container">
			<h1>iocasts' hook-server</h1>
			<h3>Global configuration</h3>
			<p>The following table shows you the base configuration of your hook server.</p>
			<dl>
				<dt>Base template:</dt>
				<dd>{{config["template"]}}</dd>
				<dt>Sender eMail:</dt>
				<dd>{{config["mailer"]["sender"]}}</dd>
				<dt>SMTP:</dt>
				<dd>{{re.sub("(?<=:)([^@:]+)(?=@[^@]+$)", "*****", config["mailer"]["smtp"])}}</dd>
			</dl>
			<h3>Repositories</h3>
			<p>List of all configured repositories in your <strong>iocast-hook-server.json</strong> file.</p>
			<div class="tree">
				<ul>
					% for idx in config["repos"]:
					% 	tmpl = config["repos"][idx]["template"] if "template" in config["repos"][idx] else config["template"]
					<li>
						<div><strong>{{idx}}</strong></div>
						<ul>
							<li>
								<div style="min-width: 170px;"><strong>Template:</strong></div>
								<div>{{tmpl}}</div>
							</li>
							<li>
								<div style="min-width: 170px;"><strong>Notification:</strong></div>
								<div>{{config["repos"][idx]["notification"]}}</div>
							</li>
							<li>
								<div style="min-width: 170px;"><strong>Branches:</strong></div>
								<ul>
									% for branch in config["repos"][idx]["branches"]:
									<li>
										<div style="min-width: 130px;">{{branch}}</div>
										<div>{{config["repos"][idx]["branches"][branch]["local"]}}</div>
									</li>
									% end
								</ul>
							</li>
						</ul>
					</li>
					% end
				</ul>
			</div>
		</div>
	</body>
</html>

