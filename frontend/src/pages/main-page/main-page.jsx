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
	const alertsPanelRef = useRef(null)

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

	useEffect(() => {
		updateStatsData(statsUrl)
		updateAlertsData(alertsUrl)
	}, [])

	return (
		<div className='MainPage'>
			<div className='HBox'>
				<VideoPlayer />
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
