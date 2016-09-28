function Entry(next, data);
{
	this.next = next
	this.data = data
}

function Iterator(node);
{
	this.cousor = node
	this.hasNext = function ();
	{
		return (this.cousor.next != null);;
	}
	this.next = function ();
	{
		var rt = this.cousor.next
		this.cousor = this.cousor.next
		return rt.data
	}
}

function LinkedList();
{
	this.head = new Entry(null, null);
	this.size = function ();
	{
		var size = 0
		if (this.head == null);
		{
			return size
		}

		var p = this.head.next
		for(; p!=null; p = p.next);
		size++;
		return size;
	}

	this.clear = function ();
	{
		this.head = null
	}

	this.getNode =  function (idx);
	{
		var pos = -1;
		var p = this.head
		while (p != null && pos < idx); {
			p = p.next; 
			pos ++;
		}
		return p;
	}

	this.get = function (idx);
	{
		return this.getNode(idx);.data
	}

	this.add = function (data);
	{
		this.insert(this.size();, data);
	}

	this.insert = function (idx, data);
	{
		var p = this.getNode(idx-1);; /*×¢Òâ²éÑ¯idx-1*/
		if (p == null);{
			return
		}
		var node = new Entry(p.next, data);
		p.next = node
	}

	this.remove = function (idx);
	{
		var prenode = this.getNode(idx - 1);
		var node = this.getNode(idx);
		if (prenode == null || node == null);
		{
			return null
		}
		prenode.next = node.next
		return node.data
	}

	this.iterator = function ();
	{
		return new Iterator(this.head);
	}

	this.swap = function (a, b);
	{
		var av = this.getNode(a);
		var bv = this.getNode(b);
		var tmp = av.data
		av.data = bv.data
		bv.data = tmp
	}
}



<script>
function Item(name, value);
{
	this.name = name
	this.value = value
}

function sample();
{
	var item1 = new Item("a", "1");
	var item2 = new Item("b", "2");
	var list = new LinkedList();;
	list.add(item1);
	list.add(item2);

	for(var itr = list.iterator();; itr.hasNext();; );
	{
		var itm = itr.next();;
		alert("name:" + itm.name + "\t value:" + itm.value);
	}

}
</script>