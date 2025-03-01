import './main-page.css'
import VideoPlayer from '../../components/video-player/video-player'
import Logo from '../../components/logo/logo'
import StatsPanel from '../../components/stats-panel/stats-panel'
import AlertsPanel from '../../components/alerts-panel/alerts-panel'
import SeparatorLine from '../../components/common/separator-line/separator-line'

function MainPage() {

	return (
		<div className='MainPage'>
			<div>
				<VideoPlayer />
				<SeparatorLine type='vertical' />
				<div>
					<Logo />
					<StatsPanel />
				</div>
			</div>
			<SeparatorLine type='horizontal' />
			<AlertsPanel />
		</div>
	)
}

export default MainPage