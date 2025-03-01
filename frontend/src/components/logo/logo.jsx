import './logo.css'
import LogoSVG from '../../assets/aether-logo.svg'

function Logo() {

	return (
		<div className='Logo'>
			<img
				src={LogoSVG}
				alt='AetherLogo'
				className='LogoImage'
			/>
		</div>
	)
}

export default Logo