DrawRectangle = function(id, onMouseUp, className){  
	
	document.oncontextmenu=function() {  
       return true;  
    };
	    
    this.IMG = document.getElementById(id);  
    
    var masker = document.createElement("div");
    masker.id = "mask_" + id;
    var position = this.getAbsolutePosition(this.IMG);
    
    masker.style.width = position.width + "px";
    masker.style.height = position.height + "px";
    masker.style.left = position.left;
    masker.style.top = position.top;
    masker.style["background-image"] = "url("+this.IMG.src+")";
    masker.className = "imgmasker";

    this.masker = masker;
    this.IMG.parentNode.appendChild(masker);
    this.IMG.parentNode.removeChild(this.IMG);
    
    this.isDraw = false;  
    this.isMouseUp = true;  
    this.index = 0;  
    this.currentDrawRectangle = null;  
    this.className = className;  
      
    this.RectangleDivs = [];  
      
    this.debug = true;  
  
    this._onMouseUp = onMouseUp;  
      
    this.bindListener();  
};
  
DrawRectangle.prototype = {  
    bindListener: function(){  
      
        this.masker.onmousemove = this.dragSize.bind(this);  
        this.masker.onmouseup = this.onMouseUp.bind(this);  
        this.masker.onmouseout = this.onMouseOut.bind(this);  
        this.masker.onmouseover = this.onMouseOver.bind(this);  
        this.masker.onmousedown = this.drawLayer.bind(this);  
        this.masker.onmouseup = this.onMouseUp.bind(this);  
    },  
    drawLayer: function(){  
        //this.IMG.setCapture(true);  
        this.isDraw = true;  
        this.ismouseup = false;  
        this.index++;  
          
        var pos = this.getSourcePos();  
          
        var x = event.offsetX;   
        var y = event.offsetY;   
  
        var top = y + pos.top - 2;  
        var left = x + pos.left - 2;  
         
        var d = document.createElement("div");  
       // document.body.appendChild(d);
        this.masker.appendChild(d);
        d.style.border = "1px solid #ff0000";  
        d.style.width = 0;  
        d.style.height = 0;  
        d.style.overflow = "hidden";  
        d.style.position = "absolute";  
        d.style.left = left + "px";
        d.style.top = top + "px"; 
        d.style.opacity = 0.5;
        
        d.style["z-index"] = 2;
        if(this.className) {  
            d.className = this.className;  
        }  
        d.id = "draw" + this.index;  
        if (this.debug) {  
            d.innerHTML = "<div class='innerbg'>x:" + x + ",y:" + y + "..</div>";  
        }  
          
        this.currentDrawRectangle = d;  
          
        this.RectangleDivs[this.index] = {  
            left: left,  
            top: top,  
            el: d  
        };  
    },  
    getSourcePos: function(){  
        return this.getAbsolutePosition(this.masker);  
    },  
    dragSize: function(){  
        if (this.isDraw) {
            if (!(event.srcElement.tagName.toLowerCase() == "div" && event.srcElement.className == "imgmasker"))   
                return;  
              
            var pos = this.getSourcePos();  
            var img_x = pos.top;   
            var img_y = pos.left;   
            var x = event.offsetX;  
            var y = event.offsetY;  
            var drawW = (x + img_x) - this.RectangleDivs[this.index].left;  
            var drawH = (y + img_y) - this.RectangleDivs[this.index].top;  
            this.currentDrawRectangle.style.width = (drawW > 0 ? drawW : -drawW) + "px";  
            this.currentDrawRectangle.style.height = (drawH > 0 ? drawH : -drawH) + "px"; 
            if (drawW < 0) {  
                this.currentDrawRectangle.style.left = (x + img_x) + "px";   
            }  
            if (drawH < 0) {  
                this.currentDrawRectangle.style.top = (y + img_y) + "px";    
            }  
              
            if (this.debug) {  
                this.currentDrawRectangle.innerHTML = "<div class='innerbg'>x:" + x + ",y:" + y +  
                ". img_x:" +  
                img_x +  
                ",img_y:" +  
                img_y +  
                ". drawW:" +  
                drawW +  
                ",drawH:" +  
                drawH +  
                ".  Dleft[i]:" +  
                this.RectangleDivs[this.index].left +  
                ",Dtop[i]:" +  
               this.RectangleDivs[this.index].top +  
                "src:" +  
                event.srcElement.tagName +  
                ",this.isDraw: " + this.isDraw +
                ",this.isMouseUp: " + this.isMouseUp +
                ".</div>";  
            }  
              
        }  
        else {  
            return false;  
        }  
    },  
      
    stopDraw: function(){  
        this.isDraw = false;  
    },  
      
    onMouseOut: function(){  
        if (!this.isMouseUp) {  
            this.isDraw = false;  
        }  
    },  
      
    onMouseUp: function(){  
        this.isDraw = false;  
        this.isMouseUp = true;  
        //this.IMG.releaseCapture();  
  
        if(this._onMouseUp) {  
            this._onMouseUp.call(this, this.currentDrawRectangle);  
        }  
    },  
      
    onMouseOver: function(){  
        if (!this.isMouseUp) {  
            this.isDraw = true;  
        }  
    },  
      
    getAbsolutePosition: function(obj){  
        var t = obj.offsetTop;  
        var l = obj.offsetLeft;  
        var w = obj.offsetWidth;  
        var h = obj.offsetHeight;  
          
        while (obj = obj.offsetParent) {  
            t += obj.offsetTop;  
            l += obj.offsetLeft;  
        }  
          
        return {  
            top: t,  
            left: l,  
            width: w,  
            height: h  
        };
    }  
};