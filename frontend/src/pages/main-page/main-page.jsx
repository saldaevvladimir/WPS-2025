import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import './main-page.css'
import VideoPlayer from '../../components/video-player/video-player'
import Logo from '../../components/logo/logo'
import StatsPanel from '../../components/stats-panel/stats-panel'
import AlertsPanel from '../../components/alerts-panel/alerts-panel'
import SeparatorLine from '../../components/common/separator-line/separator-line'

function MainPage() {
	const [stats, setStats] = useState([])
	const [imageSrc, setImageSrc] = useState(null)
	const alertsPanelRef = useRef(null)

	const videoSrc = 'videoSrc.m3u8'
	const statsUrl = 'api/stats'
	const alertsUrl = 'api/alerts'

	async function updateStatsData(statsUrl) {
		try {
			const response = await axios.get(statsUrl)
			setStats(response.data)
		} catch (error) {
			console.error('Error fetching stats data:', error)
		}
	}

	async function updateAlertsData(alertsUrl) {
		try {
			const response = await axios.get(alertsUrl)
			console.log(response.data)
			response.data.forEach((alert) => {
				alertsPanelRef.current.addAlert(alert)
			})
		} catch (error) {
			console.error('Error fetching alerts data:', error)
		}
	}

	function updateStats(stats) {
		setStats(stats)
	}

	function updateAlerts(alerts) {
		alerts.forEach((alert) => {
			alertsPanelRef.current.addAlert(alert)
		})
	}

	function updateData(data) {
		const stats = [{
			'name': 'Количество особей',
			'value': data['population_size'],
		}]
		const alerts = data['alerts'] || []

		if (data['frame_with_boxes']) {
			setImageSrc(data['frame_with_boxes'])
		}

		updateStats(stats)
		updateAlerts(alerts)
	}

	async function setupWebSocket() {
		const socket = new WebSocket(`ws://127.0.0.1:8000/ws/laboratory/`)

		socket.onmessage = (event) => {
			const data = JSON.parse(event.data).state
			console.log('WebSocket data:', data)

			updateData(data)
		}

		socket.onopen = () => {
			console.log('WebSocket connection opened')
		}

		socket.onclose = () => {
			console.log('WebSocket connection closed')
		}

		socket.onerror = (error) => {
			console.error('WebSocket error:', error)
		}
	}

	useEffect(() => {
		setupWebSocket()
	}, [])

	return (
		<div className='MainPage'>
			<div className='HBox'>
				<VideoPlayer videoSrc={videoSrc} imageSrc={imageSrc} />
				<SeparatorLine
					vertical={true}
					className='Separator ml-[40px] mr-[40px]'
				/>
				<div className='VBox'>
					<Logo />
					<StatsPanel stats={stats} />
				</div>
			</div>
			<SeparatorLine
				vertical={false}
				className='Separator mt-[80px] mb-[40px]'
			/>
			<AlertsPanel
				ref={alertsPanelRef}
				autoDeleteTime={20}
			/>
		</div>
	)
}

export default MainPage
