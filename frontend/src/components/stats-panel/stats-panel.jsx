import './stats-panel.css'

function StatsPanel({ stats }) {

	return (
		<div className='StatsPanel'>
			<div>
				Текущая статистика:
			</div>
			<ul className='list-disc pl-10'>
				{stats.map((stat, index) => (
					<li key={index}>
						{stat.name}: {stat.value}
					</li>
				))}
			</ul>
		</div>
	)
}

export default StatsPanel