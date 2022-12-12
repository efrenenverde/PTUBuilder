import classes from './FeatHolder.module.css'

const FeatHolder = (props) => {
    //const params = useParams();

return <div className={classes.holder}>
    <h1>Feat: {props.Name}</h1>
    <ul>
        <li>{props.Effect}</li>
        <li>{props.Freq}</li>
        <li>{props.Tags}</li>
    </ul>
</div>
}

export default FeatHolder;