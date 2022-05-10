import React, { useRef, useEffect } from 'react'
import useCanvas from './useCanvas'

var lastOffsetWidth = 0;
var lastOffsetHeight = 0;

const Canvas = props => {

    const { draw, ...rest } = props
    // const { draw, postdraw=_postdraw, ...rest } = props
    // const canvasRef = useCanvas(draw, {predraw, postdraw})
    const canvasRef = useRef(null)

    // canvasRef.current.style.width ='100%';
    // canvasRef.current.style.height='100%';
    // canvasRef.current.style.position = 'absolute';

    useEffect(() => {

        const canvas = canvasRef.current
        const context = canvas.getContext('2d')
        let frameCount = 0
        let animationFrameId

        const drawLine = (x0, y0, x1, y1, color, emit) => {
            context.beginPath();
            context.moveTo(x0, y0);
            context.lineTo(x1, y1);
            context.strokeStyle = color;
            context.lineWidth = 2;
            context.stroke();
            context.closePath();

            if (!emit) { return; }
            const w = canvas.width;
            const h = canvas.height;

            socketRef.current.emit('drawing', {
                x0: x0 / w,
                y0: y0 / h,
                x1: x1 / w,
                y1: y1 / h,
                color,
            });
        };
        const clear = () => {
            context.clearRect(0, 0, canvas.width, canvas.height);
        };

        const render = ctx => {
            ctx.save()
            if (lastOffsetWidth !== canvas.offsetWidth || lastOffsetHeight !== canvas.offsetHeight) {
                lastOffsetWidth = canvas.offsetWidth;
                lastOffsetHeight = canvas.offsetHeight;
                canvas.width  = canvas.offsetWidth;
                canvas.height = canvas.offsetHeight;
            }
            var data = draw()
            if (data['type'] == "drawLine") {
                drawLine(data['startX'], data['startY'], data['endX'], data['endY'])
            } else if (data['type'] == "clear") {
                clear();
            }
            ctx.restore()

            frameCount++
            animationFrameId = requestAnimationFrame(() => render(ctx))
        }
        render(context)

        return () => {
            window.cancelAnimationFrame(animationFrameId)
        }
    }, [draw])

    return <canvas ref={canvasRef} {...rest} style={{height: '100%', width: '100%', position: 'absolute'}}/>
}

export default Canvas