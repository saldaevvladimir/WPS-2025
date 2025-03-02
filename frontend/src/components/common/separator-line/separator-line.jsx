import './separator-line.css'

function SeparatorLine({ vertical = false, className = '' }) {

	return (
		<div className={`${vertical ? 'border-l' : 'border-t'} ${className}`}>

		</div>
	)
}

export default SeparatorLine