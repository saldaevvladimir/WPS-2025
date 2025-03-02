import React, { useEffect, useRef } from 'react'
import Hls from 'hls.js'
import './video-player.css'

function VideoPlayer({ videoSrc }) {
	const videoRef = useRef(null)

	useEffect(() => {
		let hls
		const video = videoRef.current

		if (Hls.isSupported()) {
			hls = new Hls({
				autoStartLoad: true,
				debug: false,
				manifestLoadingTimeOut: 200000
			})
			hls.loadSource(videoSrc)
			hls.attachMedia(video)
			hls.on(Hls.Events.MANIFEST_PARSED, function() {
				video.play()
			})
		} else if (video.canPlayType('application/vnd.apple.mpegurl')) {
			video.src = videoSrc
			video.addEventListener('loadedmetadata', function() {
				video.play()
			})
		}

		return () => {
			if (hls) {
				hls.destroy()
			}
		}
	}, [videoSrc])

	return (
		<div className='VideoPlayer'>
			<video
				ref={videoRef}
				autoPlay
				muted
				playsInline
			/>
		</div>
	)
}

export default VideoPlayer